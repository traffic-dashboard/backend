from typing import Optional, TypedDict, List
import httpx
import os

CCTV_API_URL  = "https://openapi.its.go.kr:9443/cctvInfo"
ITS_API_KEY    = os.getenv("ITS_API_KEY")
DEFAULT_RADIUS = 100.0 / 1110.0

class CCTVItem(TypedDict):
    coordx:  str
    coordy:  str
    cctvurl: str
    cctvname:str

def build_cctv_params(lat: float, lng: float, radius: float = DEFAULT_RADIUS) -> dict:
    """쿼리 파라미터 생성."""
    minX, maxX = lng - radius, lng + radius
    minY, maxY = lat - radius, lat + radius
    return {
        "apiKey":   ITS_API_KEY,
        "type":     "all",
        "cctvType": "1",
        "minX":     str(minX),
        "maxX":     str(maxX),
        "minY":     str(minY),
        "maxY":     str(maxY),
        "getType":  "json"
    }

def find_nearest_cctv(lat: float, lng: float, radius: float = DEFAULT_RADIUS) -> Optional[CCTVItem]:
    """주어진 좌표에서 가장 가까운 CCTV를 찾아 반환."""
    params = build_cctv_params(lat, lng, radius)
    resp = httpx.get(CCTV_API_URL, params=params, timeout=5.0)
    resp.raise_for_status()
    data = resp.json()
    raw_items = data.get("body", {}).get("items")
    if raw_items is None:
        raw_items = data.get("response", {}).get("data", [])
    cctvs: List[CCTVItem] = []
    for i in raw_items or []:
        if all(k in i for k in ("coordx", "coordy", "cctvurl", "cctvname")):
            cctvs.append({
                "coordx":  str(i["coordx"]),
                "coordy":  str(i["coordy"]),
                "cctvurl": i["cctvurl"],
                "cctvname":i["cctvname"]
            })
    best = None
    best_d2 = float("inf")
    for c in cctvs:
        dx = float(c["coordx"]) - lng
        dy = float(c["coordy"]) - lat
        d2 = dx*dx + dy*dy
        if d2 < best_d2:
            best, best_d2 = c, d2
    return best
