from apscheduler.schedulers.background import BackgroundScheduler
from services.traffic_service import fetch_and_save_hourly_traffic

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_save_hourly_traffic, 'cron', hour=3, minute=0)
    scheduler.start()