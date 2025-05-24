from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID, uuid4
from app.schemas.player import Player, PlayerCreate, PlayerUpdate
from app.models.player import Player as PlayerModel

router = APIRouter()

players = {}

@router.get("/", response_model=List[Player])
def list_players():
    return list(players.values())

@router.post("/", response_model=Player)
def add_player(player: PlayerCreate):
    player_id = uuid4()
    new_player = Player(id=player_id, **player.dict())
    players[player_id] = new_player
    return new_player

@router.get("/{player_id}", response_model=Player)
def get_player(player_id: UUID):
    player = players.get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.put("/{player_id}", response_model=Player)
def update_player(player_id: UUID, player_update: PlayerCreate):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    updated_player = Player(id=player_id, **player_update.dict())
    players[player_id] = updated_player
    return updated_player

@router.patch("/{player_id}", response_model=Player)
def patch_player(player_id: UUID, player_update: PlayerUpdate):
    player = players.get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    updated_data = player.dict()
    update_fields = player_update.dict(exclude_unset=True)
    updated_data.update(update_fields)
    updated_player = Player(**updated_data)
    players[player_id] = updated_player
    return updated_player

@router.delete("/{player_id}")
def delete_player(player_id: UUID):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    del players[player_id]
    return {"detail": "Player deleted"}