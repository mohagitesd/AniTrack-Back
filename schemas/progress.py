from pydantic import BaseModel
from typing import Optional

class ProgressCreate(BaseModel):
    work_id: str
    type: str
    status: str
    current_episode: Optional[int] = 0
    current_chapter: Optional[int] = 0
