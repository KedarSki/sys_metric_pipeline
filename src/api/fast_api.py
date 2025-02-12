import os
from fastapi import FastAPI, HTTPException, Query, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv
import json
import logging
import pykx as kx



class MetricData(BaseModel):
    instance_id: str
    cpu_core: int
    cpu_mode: str
    cpu_time_usage: float
    ram_usage: int
    disk_device: str
    disk_usage: float
    timestamp: float


app = FastAPI()
app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

load_dotenv()
ip_connection = os.getenv("DATABASE_IP")
port_connection = int(os.getenv("DATABASE_PORT", 5000))


if not ip_connection or not port_connection:
    raise ValueError("DATABASE_IP and DATABASE_PORT must be set!")

try:
    conn = kx.QConnection(host=ip_connection, port=port_connection)
except Exception as e:
    print(f"Exception error: {e}")

conn(
    """
    cpu:([] instance_id:`symbol$(); cpu_core:`int$(); cpu_mode:`symbol$(); cpu_time_usage:`float$(); timestamp:`float$());
    disk:([] instance_id:`symbol$(); disk_device:`symbol$(); disk_usage:`float$(); timestamp:`float$());
    ram:([] instance_id:`symbol$(); ram_usage:`int$(); timestamp:`float$());
    .u.upd:{[table; data] table insert data};

    """
)

templates = Jinja2Templates(directory="src/app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/metrics")
async def receive_metrics(metric_data: MetricData):
    try:
        cpu_list = kx.Table(
            data={
                "instance_id": [kx.SymbolAtom(metric_data.instance_id)],
                "cpu_core": [metric_data.cpu_core],
                "cpu_mode": [kx.SymbolAtom(metric_data.cpu_mode)],
                "cpu_time_usage": [metric_data.cpu_time_usage],
                "timestamp": [metric_data.timestamp],
            }
        )
        conn(".u.upd", "cpu", cpu_list)

        disk_list = kx.Table(
            data={
                "instance_id": [kx.SymbolAtom(metric_data.instance_id)],
                "disk_device": [kx.SymbolAtom(metric_data.disk_device)],
                "disk_usage": [metric_data.disk_usage],
                "timestamp": [metric_data.timestamp],
            }
        )
        conn(".u.upd", "disk", disk_list)

        ram_list = kx.Table(
            data={
                "instance_id": [kx.SymbolAtom(metric_data.instance_id)],
                "ram_usage": [metric_data.ram_usage],
                "timestamp": [metric_data.timestamp],
            }
        )
        conn(".u.upd", "ram", ram_list)

        return {"status": "success", "message": "Data stored successfully"}

    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail=f"Error storing data: {e}")


@app.get("/metrics")
async def provide_metrics(instance_id: str = Query(description="Filter by instance ID")):

    try:
        instance_id = instance_id.strip()
        if instance_id is None or instance_id.strip() == '""' or instance_id == "''":
            raise HTTPException(status_code=400, detail="Instance ID cannot be empty")

        cpu_data = conn(f"cpu_json:.j.j select from cpu where instance_id=`{instance_id}; cpu_json")
        disk_data = conn(f"disk_json:.j.j select from disk where instance_id=`{instance_id}; disk_json")
        ram_data = conn(f"ram_json:.j.j select from ram where instance_id=`{instance_id}; ram_json")

        return {
            "cpu": json.loads(str(cpu_data)),
            "disk": json.loads(str(disk_data)),
            "ram": json.loads(str(ram_data))
        }

    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json({data})