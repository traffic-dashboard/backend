# init_db.py
from app.database import Base, engine
from app.models.traffic import HourlyTraffic
Base.metadata.create_all(bind=engine)
