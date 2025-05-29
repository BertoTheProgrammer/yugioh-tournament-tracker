from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import tournament as tournament_schema
from app.models import tournament as tournament_model
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=tournament_schema.Tournament)
def create_tournament(tour: tournament_schema.TournamentCreate, db: Session = Depends(get_db)):
    db_tour = tournament_model.Tournament(**tour.dict())
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour

@router.get("/", response_model=list[tournament_schema.Tournament])
def read_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(tournament_model.Tournament).offset(skip).limit(limit).all()
