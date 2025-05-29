import uuid
from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=True)
    format = Column(String, nullable=True)  # e.g., Standard, Goat, etc.
    is_active = Column(Boolean, default=True)

    matches = relationship("Match", back_populates="tournament", cascade="all, delete-orphan")
   
