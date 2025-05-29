from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class MatchBase(BaseModel):
    tournament_id: UUID
    player_1_id: UUID
    player_2_id: UUID
    round_number: int
    result_notes: Optional[str] = None
    winner_id: Optional[UUID] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    result_notes: Optional[str]
    winner_id: Optional[UUID]

class Match(MatchBase):
    id: UUID
    timestamp: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
