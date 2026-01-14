from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from statistics import mean
import json
import math
import os

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry data once (serverless-safe: small file)
BASE_DIR = os.path.dirname(__file__)
TELEMETRY_FILE = os.path.join(BASE_DIR, "telemetry.json")

with open(TELEMETRY_FILE, "r", encoding="utf-8") as f:
    telemetry_data = json.load(f)


def p95(values):
    """
    True 95th percentile using nearest-rank method
    """
    if not values:
        return None
    values = sorted(values)
    k = math.ceil(0.95 * len(values)) - 1
    return values[k]


@app.post("/api/telemetry")
async def telemetry(request: Request):
    payload = await request.json()
    # return {"status": "ok"}

    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms")

    results = {}

    for region in regions:
        region_records = [
            r for r in telemetry_data if r.get("region") == region
        ]

        latencies = [r["latency_ms"] for r in region_records]
        uptimes = [r["uptime"] for r in region_records]

        results[region] = {
            "avg_latency": mean(latencies) if latencies else None,
            "p95_latency": p95(latencies),
            "avg_uptime": mean(uptimes) if uptimes else None,
            "breaches": sum(
                1 for r in region_records
                if r["latency_ms"] > threshold
            ),
        }

    return results
