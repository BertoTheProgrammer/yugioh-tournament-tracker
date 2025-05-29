from sqlalchemy import Column, Integer, String, Date, Boolean
from app.database import Base

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=True)
    format = Column(String, nullable=True)  # e.g., Standard, Goat, etc.
    is_active = Column(Boolean, default=True)
