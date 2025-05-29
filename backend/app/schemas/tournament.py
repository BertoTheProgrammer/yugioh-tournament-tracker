from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class TournamentBase(BaseModel):
    name: str
    date: date
    location: Optional[str] = None
    format: Optional[str] = None
    is_active: Optional[bool] = True

class TournamentCreate(TournamentBase):
    pass

class Tournament(TournamentBase):
    id: UUID

    class Config:
        orm_mode = True