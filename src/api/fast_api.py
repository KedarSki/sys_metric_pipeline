from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
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

try:
    conn = kx.QConnection(host="172.22.170.205", port=5000)
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
        raise HTTPException(status_code=500, detail=f"Error storing data: {e}")


@app.get("/metrics")
async def provide_metrics(instance_id: str = Query(..., description="Filter by instance ID")):

    try:
        formatted_instance_id = instance_id.strip().replace('"', "")
        cpu_data = conn(f"cpu_json:.j.j select from cpu where instance_id=`{formatted_instance_id}; cpu_json")
        disk_data = conn(f"disk_json:.j.j select from disk where instance_id=`{formatted_instance_id}; disk_json")
        ram_data = conn(f"ram_json:.j.j select from ram where instance_id=`{formatted_instance_id}; ram_json")

        return {
            "cpu": json.loads(str(cpu_data)),
            "disk": json.loads(str(disk_data)),
            "ram": json.loads(str(ram_data)),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")
