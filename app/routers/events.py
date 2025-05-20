from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.event_service import fetch_events

router = APIRouter(prefix="/traffic-events", tags=["events"])

@router.get("", summary="교통사고 이벤트 조회")
def get_events():
    try:
        return fetch_events()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
