from pydantic import BaseModel
from datetime import datetime


class SurfCacheCreate(BaseModel):
    spot_name: str
    rating: float
    wind_direction: str
    swell_height: float
    tide_state: str


class SurfCacheOut(BaseModel):
    spot_name: str
    rating: float
    wind_direction: str
    swell_height: float
    tide_state: str
    timestamp: datetime

    class Config:
        orm_mode = True

