import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.scheduler.task_scheduler import start_scheduler
from app.routers import traffic, events, cctv, vehicle

load_dotenv()

required_env = ["TRAFFIC_API_KEY", "TRAFFIC_PRODUCT_ID", "ITS_API_KEY", "CORS_ORIGINS"]
missing = [k for k in required_env if not os.getenv(k)]
if missing:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

app = FastAPI(title="Traffic & CCTV API")
start_scheduler()

origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic.router)
app.include_router(events.router)
app.include_router(cctv.router)
app.include_router(vehicle.router)
