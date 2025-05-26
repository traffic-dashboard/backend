from sqlalchemy.orm import Session
from app.models.traffic import HourlyTraffic
from datetime import date

def save_hourly_traffic(db: Session, region: str, data: list[dict]):
    for item in data:
        db_entry = HourlyTraffic(
            region=region,
            date=date.today(),
            hour=item.get("hour"),
            traffic=item.get("traffic")
        )
        db.add(db_entry)
    db.commit()
