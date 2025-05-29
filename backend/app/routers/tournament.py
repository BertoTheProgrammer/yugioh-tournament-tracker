from fastapi import APIRouter, Depends, HTTPException
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas import tournament as tournament_schema
from app.models import tournament as tournament_model
from app.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=tournament_schema.Tournament)
async def create_tournament(tour: tournament_schema.TournamentCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Received tournament creation request: {tour}")
    db_tour = tournament_model.Tournament(**tour.dict())
    db.add(db_tour)
    await db.commit()
    await db.refresh(db_tour)
    logger.info(f"Tournament created with ID: {db_tour.id}")
    return db_tour

@router.get("/", response_model=list[tournament_schema.Tournament])
async def read_tournaments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    logger.info(f"Reading tournaments, skip={skip}, limit={limit}")
    result = await db.execute(select(tournament_model.Tournament).offset(skip).limit(limit))
    tournaments = result.scalars().all()
    logger.info(f"Retrieved {len(tournaments)} tournaments")
    return tournaments
