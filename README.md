# Real-Time Traffic Visualization System (Powered by FastAPI)

This project utilizes public traffic APIs to collect, visualize, and analyze real-time traffic data.

## 📦 Tech Stack

- **FastAPI**: Backend framework  
- **Python 3.12**  
- **SQLAlchemy**: ORM  
- **SQLite**: Local database for testing  
- **Redis**: Caching server  
- **Uvicorn**: ASGI server  
- **APScheduler**: Task scheduling (planned)  
- **Swagger UI**: API documentation (`/docs`)

## 🗂 Main Features & API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/traffic` | Total traffic volume for all cities |
| `/traffic/hourly` | Hourly average traffic volume per region |
| `/traffic/hourly-speed` | Hourly average speed per region |
| `/traffic/vehicle-share` | Vehicle type distribution per region |
| `/traffic/average-stats` | Daily average volume/speed per region |
| `/traffic-events/daily-count` | Regional accident count for the past 8 days |

## 📁 Project Structure

```
app/
├── routers/               # API routers
├── services/              # Data processing, caching
├── repositories/          # Database interaction
├── models/                # SQLAlchemy table definitions
├── schemas/               # Pydantic response models
├── database.py            # DB connection settings
├── init_db.py             # DB table initialization script
├── constants.py           # Constants like region names
└── main.py                # FastAPI entry point
```

## 🧪 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database tables
python -m app.init_db

# Start server
uvicorn app.main:app --reload

```

## 📌 Notes

- he region parameter must be one of the following: 서울, 청주, 전주, 광주, 서해안, 부산, 강원, 경기, 대전, 대구, 천안
- You can explore all API responses via Swagger UI: http://localhost:8000/docs

---