from pydantic import BaseModel
from typing import Optional

class RatingCreate(BaseModel):
    work_id: str  # ID Anilist ou local
    rating: int  # 1 à 10
    review: Optional[str] = None