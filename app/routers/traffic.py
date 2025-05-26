from typing import List
from fastapi import APIRouter, HTTPException
from app.constants import ALLOWED_REGIONS
from app.services.traffic_service import fetch_city_traffic
from app.services.traffic_service import fetch_average_speed_and_volume
from app.services.traffic_service import fetch_hourly_speed_by_region
from app.services.traffic_service import fetch_vehicle_share_by_region
from app.services.traffic_service import fetch_hourly_traffic_by_region
from schemas.traffic_schemas import HourlyTraffic, HourlySpeed, VehicleShare

router = APIRouter(prefix="/traffic", tags=["traffic"])

@router.get("", summary="도시별 교통량 조회", description="전체 도시의 당일 교통량 합계를 조회합니다.")
def get_traffic():
    date, totals = fetch_city_traffic()
    return {
        "date":   date,
        "cities": [{"cityName": k, "totalTraffic": v} for k, v in totals.items()]
    }

@router.get("/average-stats", summary="도시별 평균 교통량 및 평균 속도 조회", description="선택한 지역의 하루 평균 교통량과 차량 속도를 반환합니다.")
def get_average_stats(region: str):
    if region not in ALLOWED_REGIONS:
        raise HTTPException(status_code=400, detail="지원하지 않는 지역입니다.")
    return fetch_average_speed_and_volume(region)

@router.get("/hourly-speed", summary="시간대별 평균 속도 조회", description="선택한 지역의 시간대별 평균 차량 속도를 조회합니다.", response_model=List[HourlySpeed])
def get_hourly_speed(region: str):
    if region not in ALLOWED_REGIONS:
        raise HTTPException(status_code=400, detail="지원하지 않는 지역입니다.")
    return fetch_hourly_speed_by_region(region)

@router.get("/vehicle-share", summary="차종 비율 조회", description="선택한 지역의 차량 종류별 비율(%) 데이터를 조회합니다.", response_model=List[VehicleShare])
def get_vehicle_share(region: str):
    if region not in ALLOWED_REGIONS:
        raise HTTPException(status_code=400, detail="지원하지 않는 지역입니다.")
    return fetch_vehicle_share_by_region(region)

@router.get("/hourly", summary="시간대별 교통량 조회", description="선택한 지역의 시간대별 전체 교통량 데이터를 조회합니다.", response_model=List[HourlyTraffic])
def get_hourly_traffic(region: str):
    if region not in ALLOWED_REGIONS:
        raise HTTPException(status_code=400, detail="지원하지 않는 지역입니다.")
    return fetch_hourly_traffic_by_region(region)
