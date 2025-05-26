from typing import List
from fastapi import APIRouter
from app.services.traffic_service import fetch_city_traffic
from app.services.traffic_service import fetch_average_speed_and_volume
from app.services.traffic_service import fetch_hourly_speed_by_region
from app.services.traffic_service import fetch_vehicle_share_by_region
from app.services.traffic_service import fetch_hourly_traffic_by_region
from schemas.traffic_schemas import HourlyTraffic, HourlySpeed, VehicleShare

router = APIRouter(prefix="/traffic", tags=["traffic"])

@router.get("", summary="도시별 교통량 조회")
def get_traffic():
    date, totals = fetch_city_traffic()
    return {
        "date":   date,
        "cities": [{"cityName": k, "totalTraffic": v} for k, v in totals.items()]
    }

@router.get("/average-stats", summary="도시별 평균 교통량 및 평균 속도 조회")
def get_average_stats():
    return fetch_average_speed_and_volume()

@router.get("/hourly-speed", response_model=List[HourlySpeed])
def get_hourly_speed(region: str):
    return fetch_hourly_speed_by_region(region)


# Vehicle share by region endpoint
@router.get("/vehicle-share", response_model=List[VehicleShare])
def get_vehicle_share(region: str):
    return fetch_vehicle_share_by_region(region)

@router.get("/hourly", response_model=List[HourlyTraffic])
def get_hourly_traffic(region: str):
    return fetch_hourly_traffic_by_region(region)
