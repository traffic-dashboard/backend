import os
import httpx

from datetime import datetime
from collections import defaultdict
from app.services.traffic_service import REGION_TO_CITY

EVENT_API_URL = "https://openapi.its.go.kr:9443/eventInfo"
ITS_API_KEY   = os.getenv("ITS_API_KEY")

if not ITS_API_KEY:
    raise RuntimeError("ITS_API_KEY not set")

def fetch_events() -> dict:
    """교통사고 이벤트를 가져와 필수 필드만 반환."""
    params = {
        "apiKey":     ITS_API_KEY,
        "type":       "all",
        "eventType":  "all",
        "getType":    "json"
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
            "coordY":          i.get("coordY")
        }
        for i in items
    ]
    return {"totalCount": body.get("totalCount", 0), "events": events}

def fetch_daily_event_count(region: str) -> int:
    today = datetime.now().strftime("%Y%m%d")
    raw = fetch_events()
    count = 0
    for e in raw.get("events", []):
        start = e.get("startDate", "")
        if not start.startswith(today):
            continue
        count += 1
    return count
