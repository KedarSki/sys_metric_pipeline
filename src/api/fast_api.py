from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Union
import pykx as kx
import json
import os


class MetricData(BaseModel):
    instance_id: str
    cpu_core: int
    cpu_mode: str
    cpu_time_usage: float
    ram_usage: int
    disk_device: str
    disk_usage: float
    date: float


app = FastAPI()
app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

try:
    conn = kx.QConnection(host="172.22.170.205", port=5000)
except Exception as e:
    print(f"Exception error{e}")

conn(
    """
    cpu:([] instance_id:`symbol$(); cpu:`int$(); mode:`symbol$(); time_of_usage:`float$(); date:`float$());
    disk:([] instance_id:`symbol$(); device:`symbol$(); usage:`float$(); date:`float$());
    ram:([] instance_id:`symbol$(); ram_usage:`int$(); date:`float$());
"""
)


@app.post("/metrics")
async def receive_metrics(metric_data: MetricData):
    return print(metric_data)


@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse("src/app/templates/index.html")
