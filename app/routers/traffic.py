from fastapi import APIRouter
from app.services.traffic_service import fetch_city_traffic
from app.services.traffic_service import fetch_average_speed_and_volume
from app.services.traffic_service import fetch_hourly_speed_by_region

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

@router.get("/hourly-speed")
def get_hourly_speed(region: str):
    return fetch_hourly_speed_by_region(region)
