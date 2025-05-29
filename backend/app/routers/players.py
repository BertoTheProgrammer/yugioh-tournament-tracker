from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.player import Player, PlayerCreate, PlayerUpdate
from app.models.player import Player as PlayerModel
from app.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

players = {}

@router.get("/", response_model=List[Player])
async def list_players(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PlayerModel))
    players = result.scalars().all()
    logger.info(f"Listed {len(players)} players")
    return players

@router.post("/", response_model=Player)
async def add_player(player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    new_player = PlayerModel(**player.dict())
    db.add(new_player)
    await db.commit()
    await db.refresh(new_player)
    logger.info(f"Added new player with ID: {new_player.id}")
    return new_player

@router.get("/{player_id}", response_model=Player)
async def get_player(player_id: UUID, db: AsyncSession = Depends(get_db)):
    player = await db.get(PlayerModel, player_id)
    if not player:
        logger.warning(f"Player with ID {player_id} not found")
        raise HTTPException(status_code=404, detail="Player not found")
    logger.info(f"Retrieved player with ID: {player_id}")
    return player

@router.put("/{player_id}", response_model=Player)
async def update_player(player_id: UUID, player_update: PlayerCreate, db: AsyncSession = Depends(get_db)):
    player = await db.get(PlayerModel, player_id)
    if not player:
        logger.warning(f"Player with ID {player_id} not found for full update")
        raise HTTPException(status_code=404, detail="Player not found")
    for key, value in player_update.dict().items():
        setattr(player, key, value)
    await db.commit()
    await db.refresh(player)
    logger.info(f"Updated player with ID: {player_id}")
    return player


@router.patch("/{player_id}", response_model=Player)
async def patch_player(player_id: UUID, player_update: PlayerUpdate, db: AsyncSession = Depends(get_db)):
    player = await db.get(PlayerModel, player_id)
    if not player:
        logger.warning(f"Player with ID {player_id} not found for patch update")
        raise HTTPException(status_code=404, detail="Player not found")
    update_fields = player_update.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(player, key, value)
    await db.commit()
    await db.refresh(player)
    logger.info(f"Patched player with ID: {player_id} - fields updated: {list(update_fields.keys())}")
    return player

@router.delete("/{player_id}")
async def delete_player(player_id: UUID, db: AsyncSession = Depends(get_db)):
    player = await db.get(PlayerModel, player_id)
    if not player:
        logger.warning(f"Player with ID {player_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Player not found")
    await db.delete(player)
    await db.commit()
    logger.info(f"Deleted player with ID: {player_id}")
    return {"detail": "Player deleted"}