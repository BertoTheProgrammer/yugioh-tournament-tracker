import uuid
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tournament_id = Column(UUID(as_uuid=True), ForeignKey("tournaments.id"), nullable=False)
    player_1_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    player_2_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    winner_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=True)
    round_number = Column(Integer, nullable=False)
    result_notes = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    tournament = relationship("Tournament", back_populates="matches")
    player_1 = relationship("Player", foreign_keys=[player_1_id])
    player_2 = relationship("Player", foreign_keys=[player_2_id])
    winner = relationship("Player", foreign_keys=[winner_id])
