from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend import models
from backend.schemas import SurfCacheCreate, SurfCacheOut

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.post("/write", response_model=SurfCacheOut)
def write_cache(data: SurfCacheCreate, db: Session = Depends(get_db)):
    new_entry = models.SurfCache(
        spot_name=data.spot_name,
        rating=data.rating,
        wind_direction=data.wind_direction,
        swell_height=data.swell_height,
        tide_state=data.tide_state
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/get/{spot_name}", response_model=SurfCacheOut)
def get_cache(spot_name: str, db: Session = Depends(get_db)):
    entry = (
        db.query(models.SurfCache)
        .filter(models.SurfCache.spot_name == spot_name)
        .order_by(models.SurfCache.timestamp.desc())
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="No cache found for that spot")
    return entry