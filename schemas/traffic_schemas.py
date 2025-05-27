from pydantic import BaseModel
from datetime import datetime

class HourlyTraffic(BaseModel):
    hour: str
    traffic: float

class HourlySpeed(BaseModel):
    hour: str
    avg_speed: float

class VehicleShare(BaseModel):
    type: str
    percentage: float

class AverageStats(BaseModel):
    average_speed: float
    average_traffic: float

class HourlyTrafficSchema(BaseModel):
    region: str
    timestamp: datetime
    traffic: int

    class Config:
        from_attributes = True
