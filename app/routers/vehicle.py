
from fastapi import APIRouter
from app.services.traffic_service import fetch_vehicle_type_share

router = APIRouter()

@router.get("/traffic/vehicle-type-share")
def get_vehicle_type_share():
    """차량 종류별 교통량 비율 반환"""
    return fetch_vehicle_type_share()
