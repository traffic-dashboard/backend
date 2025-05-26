from pydantic import BaseModel

class HourlyTraffic(BaseModel):
    hour: str
    traffic: float

class HourlySpeed(BaseModel):
    hour: str
    avg_speed: float


class VehicleShare:
    pass

class AverageStats(BaseModel):
    average_speed: float
    average_traffic: float