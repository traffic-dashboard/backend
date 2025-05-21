from database import Base, engine
from models.traffic import HourlyTraffic

Base.metadata.create_all(bind=engine)
