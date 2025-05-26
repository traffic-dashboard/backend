from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services.cctv_service import find_nearest_cctv, DEFAULT_RADIUS

router = APIRouter(prefix="/api/nearest-cctv", tags=["cctv"])

@router.get("", summary="가장 가까운 CCTV 조회")
def nearest_cctv(
    lat:    float = Query(..., description="사고 위도"),
    lng:    float = Query(..., description="사고 경도"),
    radius: float = Query(DEFAULT_RADIUS, description="검색 반경 (° 단위)")
):
    try:
        c = find_nearest_cctv(lat, lng, radius)
        if not c:
            return JSONResponse(status_code=404, content={"error": "근처 CCTV 없음"})
        return c
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
