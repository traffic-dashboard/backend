from typing import Literal
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from app.services.event_service import fetch_events, fetch_event_counts_last_8_days

router = APIRouter(prefix="/traffic-events", tags=["events"])

# ITS API가 지원하는 타입
EventType = Literal["all", "acc", "cor", "wea", "ete", "dis", "etc"]

@router.get("", summary="교통사고 이벤트 조회")
def get_events(
    eventType: EventType = Query(
      "all",
      title="eventType",
      description="조회할 이벤트 타입: all(전체), acc(사고), cor(공사), wea(기상), ete(기타돌발), dis(재난), etc(기타)"
    )
):
    try:
        return fetch_events(eventType)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/daily-count", summary="최근 8일간 이벤트 수 조회")
def get_daily_event_count(region: str):
    try:
        return {
            "region": region,
            "data": fetch_event_counts_last_8_days(region)
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
