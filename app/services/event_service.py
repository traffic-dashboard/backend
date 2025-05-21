import os
from datetime import timedelta

import httpx
from typing import Dict, List

EVENT_API_URL = "https://openapi.its.go.kr:9443/eventInfo"
ITS_API_KEY = os.getenv("ITS_API_KEY")

if not ITS_API_KEY:
    raise RuntimeError("ITS_API_KEY not set")


def _fetch_single(event_type: str) -> Dict:
    """단일 eventType으로 ITS API 호출"""
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
        "events":     events,
    }


def fetch_events(event_types: List[str]) -> Dict:
    """
    event_types 목록으로 각각 ITS API를 호출한 뒤,
    결과를 합쳐서 한 번에 반환.
    """
    # "all" 하나만 들어오면 그대로 단일 호출
    if len(event_types) == 1 and event_types[0] == "all":
        return _fetch_single("all")

    combined_events = []
    total = 0

    for et in event_types:
        data = _fetch_single(et)
        total += data["totalCount"]
        combined_events.extend(data["events"])

    return {
        "totalCount": total,
        "events":     combined_events,
    }


def fetch_event_counts_last_8_days(region: str) -> list[dict[str, int]]:
    raw = fetch_events()
    from datetime import datetime
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).strftime("%Y%m%d") for i in reversed(range(8))]

    # Initialize with 0 counts
    counts_by_date = {d: 0 for d in dates}
    for e in raw.get("events", []):
        start = e.get("startDate", "")
        date_key = start[:8]
        if date_key in counts_by_date:
            counts_by_date[date_key] += 1

    return [{"date": d, "count": counts_by_date[d]} for d in dates]
