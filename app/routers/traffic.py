from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.traffic_service import fetch_city_traffic

router = APIRouter(prefix="/traffic", tags=["traffic"])

@router.get("", summary="도시별 교통량 조회")
def get_traffic():
    try:
        date, totals = fetch_city_traffic()
        return {
            "date":   date,
            "cities": [{"cityName": k, "totalTraffic": v} for k, v in totals.items()]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
