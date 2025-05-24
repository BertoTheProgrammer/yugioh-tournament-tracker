from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional

class PlayerBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class PlayerCreate(PlayerBase):
    password: str  # only when creating player

class PlayerUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    full_name: Optional[str]

class Player(PlayerBase):
    id: UUID

    class Config:
        orm_mode = True
