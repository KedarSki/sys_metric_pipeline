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

@app.post("/metrics")
async def receive_metrics(metric_data: MetricData):
    with kx.SyncQConnection("localhost", 5000) as conn:
        print(conn("test").py())
    return print(metric_data)

@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse('src/app/templates/index.html')
