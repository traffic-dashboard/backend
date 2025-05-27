# app/services/event_service.py

import os
import httpx
from datetime import datetime, timedelta
from typing import Literal

EVENT_API_URL = "https://openapi.its.go.kr:9443/eventInfo"
ITS_API_KEY   = os.getenv("ITS_API_KEY")

if not ITS_API_KEY:
    raise RuntimeError("ITS_API_KEY not set")

# ITS API가 지원하는 이벤트 타입
EventType = Literal["all", "acc", "cor", "wea", "ete", "dis", "etc"]

def fetch_events(event_type: EventType = "all") -> dict:
    """
    event_type:
      "all"  - 전체 이벤트
      "acc"  - 교통사고
      "cor"  - 공사
      "wea"  - 기상
      "ete"  - 기타돌발
      "dis"  - 재난
      "etc"  - 기타
    """
    params = {
        "apiKey":    ITS_API_KEY,
        "type":      "all",
        "eventType": event_type,
        "getType":   "json",
    }
    resp = httpx.get(EVENT_API_URL, params=params)
    resp.raise_for_status()
    body = resp.json().get("body", {})
    items = body.get("items", [])
    events = [
        {
            "eventType":       i.get("eventType"),
            "eventDetailType": i.get("eventDetailType"),
            "startDate":       i.get("startDate"),
            "coordX":          i.get("coordX"),
            "coordY":          i.get("coordY"),
        }
        for i in items
    ]
    return {
        "totalCount": body.get("totalCount", 0),
        "events":     events
    }

def fetch_event_counts_last_8_days(region: str) -> list[dict[str, int]]:
    raw = fetch_events()  # 기본값은 all
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).strftime("%Y%m%d") for i in reversed(range(8))]

    counts_by_date = {d: 0 for d in dates}
    for e in raw.get("events", []):
        start = e.get("startDate", "")
        date_key = start[:8]
        if date_key in counts_by_date:
            counts_by_date[date_key] += 1

    return [{"date": d, "count": counts_by_date[d]} for d in dates]
