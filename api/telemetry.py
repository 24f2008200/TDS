import os
import json
import math
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# ---- Safe path to telemetry.json ----
BASE_DIR = os.path.dirname(__file__)
TELEMETRY_FILE = os.path.join(BASE_DIR, "..", "telemetry.json")

# ---- CORS headers ----
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

# ---- Helper to compute percentile ----
def percentile(values, p):
    """Compute the p-th percentile of a list of numbers"""
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    return values[f] * (c - k) + values[c] * (k - f)

# ---- Telemetry route ----
@app.api_route("/api/telemetry", methods=["POST", "OPTIONS"])
def telemetry(request: Request, payload: dict = None):
    # Handle preflight

    if request.method == "OPTIONS":
        return JSONResponse(content={}, headers=CORS_HEADERS)

    # Validate payload
    if payload is None or "regions" not in payload or "threshold_ms" not in payload:
        raise HTTPException(status_code=400, detail="Missing regions or threshold_ms")

    regions = payload["regions"]
    threshold = payload["threshold_ms"]

    # Load telemetry.json
    if not os.path.exists(TELEMETRY_FILE):
        raise HTTPException(status_code=500, detail="telemetry.json not found")

    try:
        with open(TELEMETRY_FILE, "r") as f:
            records = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read telemetry.json: {str(e)}")

    # Compute metrics per region
    result = {}
    for region in regions:
        region_records = [r for r in records if r.get("region") == region]
        latencies = [r.get("latency_ms") for r in region_records if "latency_ms" in r]
        uptimes = [r.get("uptime") for r in region_records if "uptime" in r]

        if not latencies:
            result[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0,
            }
            continue

        avg_latency = sum(latencies) / len(latencies)
        p95_latency = percentile(latencies, 95)
        avg_uptime = sum(uptimes) / len(uptimes) if uptimes else None
        breaches = sum(1 for l in latencies if l > threshold)

        result[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    # Return POST response with CORS headers
    return JSONResponse(content=result, headers=CORS_HEADERS)
