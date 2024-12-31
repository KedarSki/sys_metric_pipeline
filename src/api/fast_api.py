from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import pykx as kx


app = FastAPI()


class RamMetric(BaseModel):
    instance_id: str
    ram_usage: int
    date: date


class DiscMetric(BaseModel):
    instance_id: str
    device: str
    disc_usage: float
    date: date


class RamMetric(BaseModel):
    instance_id: str
    ram_usage: int
    date: date


@app.get("/")
async def metric():
    return kx.q("select from cpu")
