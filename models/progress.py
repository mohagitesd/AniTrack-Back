from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Progress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    work_id: str  # L’ID Anilist ou un UUID local
    type: str  # "anime" ou "manga"
    status: str  # "watching", "completed", etc.
    current_episode: Optional[int] = 0
    current_chapter: Optional[int] = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
