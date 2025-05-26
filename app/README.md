

# 실시간 교통량 시각화 시스템 (FastAPI 기반)

이 프로젝트는 공공 교통 API를 활용해 실시간 교통 데이터를 수집하고, 시각화 및 분석하는 시스템입니다.

## 📦 기술 스택

- **FastAPI**: 백엔드 프레임워크
- **Python 3.12**
- **SQLAlchemy**: ORM
- **SQLite**: 테스트용 로컬 데이터베이스
- **Redis**: 캐싱 서버
- **Uvicorn**: 서버 실행
- **APScheduler**: 자동화 예정
- **Swagger UI**: API 문서화 (`/docs`)

## 🗂 주요 기능 및 API 목록

| 엔드포인트 | 설명 |
|------------|------|
| `/traffic` | 전체 도시 교통량 총합 |
| `/traffic/hourly` | 지역별 시간대별 평균 교통량 |
| `/traffic/hourly-speed` | 지역별 시간대별 평균 속도 |
| `/traffic/vehicle-share` | 지역별 차량 종류 비율 |
| `/traffic/average-stats` | 지역별 하루 평균 교통량/속도 |
| `/traffic-events/daily-count` | 최근 8일간 지역별 사고량 통계 |

## 📁 프로젝트 구조

```
app/
├── routers/               # API 라우터
├── services/              # 데이터 처리, 캐싱
├── repositories/          # DB 저장 로직
├── models/                # SQLAlchemy 테이블 정의
├── schemas/               # Pydantic 응답 모델
├── database.py            # DB 연결 설정
├── init_db.py             # 테이블 초기화 스크립트
├── constants.py           # 지역 목록 등 고정값
└── main.py                # FastAPI 앱 실행
```

## 🧪 실행 방법

```bash
# 패키지 설치
pip install -r requirements.txt

# 테이블 생성
python -m app.init_db

# 서버 실행
uvicorn app.main:app --reload
```

## 📌 주의사항

- region 파라미터는 다음 값 중 하나여야 합니다: 서울, 청주, 전주, 광주, 서해안, 부산, 강원, 경기, 대전, 대구, 천안
- 모든 응답은 Swagger UI를 통해 확인할 수 있습니다: http://localhost:8000/docs

---