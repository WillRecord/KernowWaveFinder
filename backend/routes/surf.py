from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.schemas import SurfCacheOut
from backend.models import SurfCache

# Import your actual surf logic
from current.pipeline.run_pipeline import rate_all_spots  # your file outside folders

router = APIRouter(prefix="/surf", tags=["Surf"])


@router.get("/", response_model=List[SurfCacheOut])
def get_all_surf_ratings(db: Session = Depends(get_db)):
    """
    Runs your pipeline for ALL spots,
    saves all results to DB,
    returns a list.
    """

    results = rate_all_spots()

    # Save all to DB
    entries = []
    for r in results:
        entry = SurfCache(
            spot_name=r["spot_name"],
            rating=r["rating"],
            wind_direction=r["wind_direction"],
            swell_height=r["swell_height"],
            tide_state=r["tide_state"],
        )
        db.add(entry)
        entries.append(entry)

    db.commit()

    # refresh each entry so timestamps come back
    for e in entries:
        db.refresh(e)

    return entries
