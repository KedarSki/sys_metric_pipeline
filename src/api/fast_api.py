from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import List, Union
import pykx as kx

class MetricValue(BaseModel):
    metric_type: str  # e.g., 'cpu', 'ram', 'disk'
    value: Union[int, float]  # Metric value

class MetricData(BaseModel):
    instance_id: str
    values: List[MetricValue]
    timestamp: float

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/metrics")
async def receive_metrics(metric_data: MetricData):
    try:
        for metric in metric_data.values:
            if metric.metric_type == "cpu":
                # Example of what you might do with the CPU data
                kx.q(f"insert into cpu_usage (`{metric_data.instance_id}`, {metric.value}, {metric_data.timestamp})")
            elif metric.metric_type == "ram":
                # Handle RAM data
                kx.q(f"insert into ram_usage (`{metric_data.instance_id}`, {metric.value}, {metric_data.timestamp})")
            elif metric.metric_type == "disk":
                # Handle Disk data
                kx.q(f"insert into disk_usage (`{metric_data.instance_id}`, {metric.value}, {metric_data.timestamp})")
        return {"status": "Data processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
