from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services.event_service import fetch_events
from app.services.event_service import fetch_event_counts_last_8_days

router = APIRouter(prefix="/traffic-events", tags=["events"])


@router.get("", summary="교통 이벤트 조회")
def get_events(
    eventType: str = Query(
        "all",
        description=(
            "조회할 eventType 코드. "
            "쉼표로 구분하여 여러 타입 지정 가능. "
            "예: all, cor, acc, wea, ete, dis, etc"
        ),
    )
):
    """
    eventType:
      - all : 전체
      - cor : 공사
      - acc : 교통사고
      - wea : 기상
      - ete : 기타돌발
      - dis : 재난
      - etc : 기타

    쉼표 구분: e.g. 'acc,dis' → 교통사고 + 재난
    """
    try:
        # 쉼표로 분리하고 공백 제거
        types = [t.strip() for t in eventType.split(",") if t.strip()]
        result = fetch_events(types)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/daily-count")
def get_daily_event_count(region: str):
    return {
        "region": region,
        "data": fetch_event_counts_last_8_days(region)
    }
