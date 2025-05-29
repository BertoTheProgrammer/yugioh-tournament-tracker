from pydantic import BaseModel
from datetime import date
from typing import Optional

class TournamentBase(BaseModel):
    name: str
    date: date
    location: Optional[str] = None
    format: Optional[str] = None
    is_active: Optional[bool] = True

class TournamentCreate(TournamentBase):
    pass

class Tournament(TournamentBase):
    id: int

    class Config:
        from_attributes = True
