from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import math

app = FastAPI()

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all origins
    allow_methods=["*"],          # allow all methods (POST, OPTIONS, GET, etc.)
    allow_headers=["*"],          # allow all headers
    allow_credentials=False       # must be False when using "*"
)

# ---- File path (SAFE for Vercel) ----
BASE_DIR = os.path.dirname(__file__)
TELEMETRY_FILE = os.path.join(BASE_DIR, "..", "telemetry.json")


# ---- Helper: percentile ----
def percentile(values, p):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    return values[f] * (c - k) + values[c] * (k - f)


# ---- API ----
@app.post("/api/telemetry")
def telemetry(payload: dict):
    try:
        # ---- Validate input ----
        regions = payload.get("regions")
        threshold = payload.get("threshold_ms")

        if not regions or threshold is None:
            raise HTTPException(status_code=400, detail="Invalid payload")

        # ---- Load telemetry ----
        if not os.path.exists(TELEMETRY_FILE):
            raise HTTPException(
                status_code=500,
                detail=f"telemetry.json not found at {TELEMETRY_FILE}",
            )

        with open(TELEMETRY_FILE, "r") as f:
            records = json.load(f)

        result = {}

        for region in regions:
            region_records = [r for r in records if r.get("region") == region]

            latencies = [r["latency_ms"] for r in region_records if "latency_ms" in r]
            uptimes = [r["uptime"] for r in region_records if "uptime" in r]

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

        return result

    except HTTPException:
        raise
    except Exception as e:
        # IMPORTANT: surface error instead of silent 500
        raise HTTPException(status_code=500, detail=str(e))
