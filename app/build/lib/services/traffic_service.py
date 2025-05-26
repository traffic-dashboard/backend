import os
from collections import defaultdict
import requests
import json
from datetime import datetime
from app.services.cache_service import get_cached_value, set_cached_value
from app.repositories.traffic_repository import save_hourly_traffic
from app.database import SessionLocal
from app.constants import ALLOWED_REGIONS

TRAFFIC_API_URL     = "https://www.bigdata-transportation.kr/api"
TRAFFIC_API_KEY     = os.getenv("TRAFFIC_API_KEY")
TRAFFIC_PRODUCT_ID  = os.getenv("TRAFFIC_PRODUCT_ID")

if not TRAFFIC_API_KEY or not TRAFFIC_PRODUCT_ID:
    raise RuntimeError("TRAFFIC_API_KEY or TRAFFIC_PRODUCT_ID not set")

REGION_TO_CITY = {
    "서울경기본부": "서울", "서울춘천센터": "서울", "수도권본부": "서울",
    "부산경남본부": "부산", "부산울산센터": "부산", "신대구부산센터": "부산",
    "경기고속도로": "경기", "전북본부": "전주", "광주전남본부": "광주",
    "대구경북본부": "대구", "제2서해안고속도로": "서해안", "강원본부": "강원",
    "대전충남본부": "대전", "충북본부": "청주", "천안논산센터": "천안"
}

def fetch_city_traffic():
    params = {
        "apiKey":    TRAFFIC_API_KEY,
        "productId": TRAFFIC_PRODUCT_ID
    }
    resp = requests.get(TRAFFIC_API_URL, params=params)
    resp.raise_for_status()
    items = resp.json().get("result", {}).get("trafficRegion", [])
    if not items:
        return None, {}
    totals = defaultdict(int)
    for e in items:
        city = REGION_TO_CITY.get(e.get("regionName",""), "기타")
        totals[city] += int(e.get("trafficAmout", 0))
    date = items[0].get("sumDate")
    return date, dict(totals)

def fetch_city_traffic_with_cache():
    key = f"traffic:city:{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    cached = get_cached_value(key)
    if cached:
        return json.loads(cached)

    _, data = fetch_city_traffic()
    set_cached_value(key, json.dumps(data), ttl=300)
    return data

def fetch_average_speed_and_volume():
    key = f"traffic:avg:{datetime.now().strftime('%Y-%m-%d %H')}"
    cached = get_cached_value(key)
    if cached:
        return json.loads(cached)

    params = {
        "apiKey": TRAFFIC_API_KEY,
        "productId": TRAFFIC_PRODUCT_ID
    }
    resp = requests.get(TRAFFIC_API_URL, params=params)
    resp.raise_for_status()
    items = resp.json().get("result", {}).get("trafficRegion", [])
    if not items:
        return {}

    city_data = defaultdict(lambda: {"total_volume": 0, "total_speed": 0.0, "count": 0})
    for e in items:
        city = REGION_TO_CITY.get(e.get("regionName", ""), "기타")
        volume = int(e.get("trafficAmout", 0))
        speed = float(e.get("speed", 0))
        city_data[city]["total_volume"] += volume
        city_data[city]["total_speed"] += speed
        city_data[city]["count"] += 1

    result = {}
    for city, data in city_data.items():
        count = data["count"]
        result[city] = {
            "avg_volume": round(data["total_volume"] / count, 2) if count else 0,
            "avg_speed": round(data["total_speed"] / count, 2) if count else 0
        }

    set_cached_value(key, json.dumps(result), ttl=300)
    return result

def fetch_hourly_traffic_seoul():
    key = f"traffic:hourly:seoul:{datetime.now().strftime('%Y-%m-%d')}"
    cached = get_cached_value(key)
    if cached:
        return json.loads(cached)

    params = {
        "apiKey": TRAFFIC_API_KEY,
        "productId": TRAFFIC_PRODUCT_ID
    }
    resp = requests.get(TRAFFIC_API_URL, params=params)
    resp.raise_for_status()
    items = resp.json().get("result", {}).get("trafficRegion", [])
    if not items:
        return []

    hourly = defaultdict(int)
    for e in items:
        region = e.get("regionName", "")
        if REGION_TO_CITY.get(region) != "서울":
            continue
        ts = e.get("sumDate", "")
        hour = ts[8:10] if ts and len(ts) >= 10 else "??"
        hourly[hour] += int(e.get("trafficAmout", 0))

    result = [{"hour": h, "traffic": v} for h, v in sorted(hourly.items())]
    set_cached_value(key, json.dumps(result), ttl=300)
    return result


def fetch_hourly_traffic_by_region(region: str):
    key = f"traffic:hourly:{region}:{datetime.now().strftime('%Y-%m-%d')}"
    cached = get_cached_value(key)
    if cached:
        return json.loads(cached)

    params = {
        "apiKey": TRAFFIC_API_KEY,
        "productId": TRAFFIC_PRODUCT_ID
    }
    resp = requests.get(TRAFFIC_API_URL, params=params)
    resp.raise_for_status()
    items = resp.json().get("result", {}).get("trafficRegion", [])
    if not items:
        return []

    hourly = defaultdict(lambda: {"total": 0, "count": 0})
    for e in items:
        mapped_region = REGION_TO_CITY.get(e.get("regionName", ""))
        if mapped_region != region:
            continue
        ts = e.get("sumDate")
        hour = ts[8:10] if ts and len(ts) >= 10 else "??"
        hourly[hour]["total"] += int(e.get("trafficAmout", 0))
        hourly[hour]["count"] += 1

    result = [
        {"hour": h, "traffic": round(data["total"] / data["count"], 2) if data["count"] else 0}
        for h, data in sorted(hourly.items())
    ]
    set_cached_value(key, json.dumps(result), ttl=300)
    return result

def fetch_hourly_speed_by_region(region: str):
    key = f"traffic:hourly-speed:{region}:{datetime.now().strftime('%Y-%m-%d')}"
    cached = get_cached_value(key)
    if cached:
        return json.loads(cached)

    params = {
        "apiKey": TRAFFIC_API_KEY,
        "productId": TRAFFIC_PRODUCT_ID
    }
    resp = requests.get(TRAFFIC_API_URL, params=params)
    resp.raise_for_status()
    items = resp.json().get("result", {}).get("trafficRegion", [])
    if not items:
        return []

    hourly = defaultdict(lambda: {"speed_total": 0.0, "count": 0})
    for e in items:
        mapped_region = REGION_TO_CITY.get(e.get("regionName", ""))
        if mapped_region != region:
            continue
        ts = e.get("sumDate", "")
        hour = ts[8:10] if ts and len(ts) >= 10 else "??"
        speed = float(e.get("speed", 0))
        hourly[hour]["speed_total"] += speed
        hourly[hour]["count"] += 1

    result = [
        {
            "hour": h,
            "avg_speed": round(data["speed_total"] / data["count"], 2) if data["count"] else 0
        }
        for h, data in sorted(hourly.items())
    ]
    set_cached_value(key, json.dumps(result), ttl=300)
    return result

def fetch_vehicle_share_by_region(region: str):
    key = f"traffic:vehicle:{region}:{datetime.now().strftime('%Y-%m-%d')}"
    cached = get_cached_value(key)
    if cached:
        return json.loads(cached)

    params = {
        "apiKey": TRAFFIC_API_KEY,
        "productId": TRAFFIC_PRODUCT_ID
    }
    resp = requests.get(TRAFFIC_API_URL, params=params)
    resp.raise_for_status()
    items = resp.json().get("result", {}).get("trafficRegion", [])
    if not items:
        return {}

    totals_by_type = defaultdict(int)
    for e in items:
        if REGION_TO_CITY.get(e.get("regionName")) != region:
            continue
        vehicle_type = e.get("vehicleType", "미분류")
        traffic_amount = int(e.get("trafficAmout", 0))
        totals_by_type[vehicle_type] += traffic_amount

    set_cached_value(key, json.dumps(totals_by_type), ttl=300)
    return totals_by_type

def fetch_and_save_hourly_traffic():
    db = SessionLocal()
    try:
        for region in ALLOWED_REGIONS:
            data = fetch_hourly_traffic_by_region(region)
            save_hourly_traffic(db, region, data)
    finally:
        db.close()
