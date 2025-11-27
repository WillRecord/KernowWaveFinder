from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .db import Base


class SurfCache(Base):
    __tablename__ = "surf_cache"

    id = Column(Integer, primary_key=True, index=True)

    spot_name = Column(String, index=True)
    rating = Column(Float)
    wind_direction = Column(String)
    swell_height = Column(Float)
    tide_state = Column(String)

    # The timestamp when this row was created
    timestamp = Column(DateTime, default=datetime.utcnow)
