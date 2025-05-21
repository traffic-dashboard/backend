from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base  # ✅ 공용 Base를 import해서 씀

class HourlyTraffic(Base):
    __tablename__ = "hourly_traffic"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    date = Column(Date, index=True)
    hour = Column(String)
    traffic = Column(Float)