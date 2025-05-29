from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List
import logging

from app.database import get_db
from app.models.match import Match as MatchModel
from app.schemas.match import Match, MatchCreate, MatchUpdate

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=Match)
async def create_match(match: MatchCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating match: {match}")
    new_match = MatchModel(**match.dict())
    db.add(new_match)
    await db.commit()
    await db.refresh(new_match)
    logger.info(f"Match created with ID: {new_match.id}")
    return new_match

@router.get("/", response_model=List[Match])
async def list_matches(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching list of matches")
    result = await db.execute(select(MatchModel))
    matches = result.scalars().all()
    logger.info(f"Found {len(matches)} matches")
    return matches

@router.get("/{match_id}", response_model=Match)
async def get_match(match_id: UUID, db: AsyncSession = Depends(get_db)):
    logger.info(f"Retrieving match with ID: {match_id}")
    match = await db.get(MatchModel, match_id)
    if not match:
        logger.warning(f"Match not found: {match_id}")
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.patch("/{match_id}", response_model=Match)
async def update_match(match_id: UUID, match_update: MatchUpdate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Updating match ID {match_id} with data: {match_update}")
    match = await db.get(MatchModel, match_id)
    if not match:
        logger.warning(f"Match not found: {match_id}")
        raise HTTPException(status_code=404, detail="Match not found")
    update_data = match_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(match, key, value)
    await db.commit()
    await db.refresh(match)
    logger.info(f"Match ID {match_id} updated")
    return match
