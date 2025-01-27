from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pykx as kx

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
    cpu:([] instance_id:`symbol$(); cpu_core:`int$(); cpu_mode:`symbol$(); cpu_time_usage:`float$(); date:`float$());
    disk:([] instance_id:`symbol$(); disk_device:`symbol$(); disk_usage:`float$(); date:`float$());
    ram:([] instance_id:`symbol$(); ram_usage:`int$(); date:`float$());
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
                "date": [metric_data.date]
            }
        )
        conn('.u.upd', 'cpu', cpu_list)

        disk_list = kx.Table(
            data={
                "instance_id": [kx.SymbolAtom(metric_data.instance_id)],
                "disk_device": [kx.SymbolAtom(metric_data.disk_device)],
                "disk_usage": [metric_data.disk_usage],
                "date": [metric_data.date]
            }
        )
        conn('.u.upd', 'disk', disk_list)

        ram_list = kx.Table(
            data={
                "instance_id": [kx.SymbolAtom(metric_data.instance_id)],
                "ram_usage": [metric_data.ram_usage],
                "date": [metric_data.date]
            }
        )
        conn('.u.upd', 'ram', ram_list)

        return {"status": "success", "message": "Data stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing data: {e}")

@app.get("/metrics")
async def provide_metrics():
    pass
@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse("src/app/templates/index.html")
