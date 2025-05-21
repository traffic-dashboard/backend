from pydantic import BaseModel

class HourlyTraffic(BaseModel):
    hour: str
    traffic: float

class HourlySpeed(BaseModel):
    hour: str
    avg_speed: float