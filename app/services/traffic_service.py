import os
from typing import Optional, Tuple
from collections import defaultdict
import requests
from dotenv import load_dotenv
import json
from datetime import datetime
from app.services.cache_service import get_cached_value, set_cached_value

load_dotenv()

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

def fetch_city_traffic() -> Tuple[Optional[str], dict[str,int]]:
    """도로별 교통량을 지역 → 도시 매핑하여 합산한 결과를 반환."""
    params = {
        "apiKey":    TRAFFIC_API_KEY,
        "productId": TRAFFIC_PRODUCT_ID
    }
    resp = requests.get(TRAFFIC_API_URL, params=params)
    resp.raise_for_status()
    items = resp.json().get("result", {}).get("trafficRegion", [])
    if not items:
        return None, {}
    totals: dict[str,int] = defaultdict(int)
    for e in items:
        city = REGION_TO_CITY.get(e.get("regionName",""), "기타")
        totals[city] += int(e.get("trafficAmout", 0))
    date = items[0].get("sumDate")
    return date, dict(totals)

def fetch_city_traffic_with_cache() -> dict[str, int]:
    key = f"traffic:city:{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    cached = get_cached_value(key)
    if cached:
        return json.loads(cached)

    _, data = fetch_city_traffic()
    set_cached_value(key, json.dumps(data), ttl=300)  # 캐시 5분 유지
    return data
