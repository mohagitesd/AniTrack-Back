from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    work_id: str  # ID Anilist ou local
    rating: int  # 1 à 10
    review: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
