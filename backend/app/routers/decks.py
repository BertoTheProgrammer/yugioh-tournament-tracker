from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import Deck, DeckCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/decks", tags=["decks"])

decks_db = []

@router.get("/", response_model=List[Deck])
async def list_decks(current_user=Depends(get_current_user)):
    return decks_db

@router.post("/", response_model=Deck)
async def create_deck(deck: DeckCreate, current_user=Depends(get_current_user)):
    new_deck = Deck(id=len(decks_db)+1, owner_id=1, **deck.dict())
    decks_db.append(new_deck)
    return new_deck

@router.get("/{deck_id}", response_model=Deck)
async def get_deck(deck_id: int, current_user=Depends(get_current_user)):
    for d in decks_db:
        if d.id == deck_id:
            return d
    raise HTTPException(status_code=404, detail="Deck not found")

@router.put("/{deck_id}", response_model=Deck)
async def update_deck(deck_id: int, deck_update: DeckCreate, current_user=Depends(get_current_user)):
    for idx, d in enumerate(decks_db):
        if d.id == deck_id:
            updated = Deck(id=deck_id, owner_id=1, **deck_update.dict())
            decks_db[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Deck not found")