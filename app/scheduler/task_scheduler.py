from apscheduler.schedulers.background import BackgroundScheduler
from app.services.traffic_service import fetch_and_save_hourly_traffic

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(fetch_and_save_hourly_traffic, 'cron', hour=3, minute=0)
    scheduler.start()