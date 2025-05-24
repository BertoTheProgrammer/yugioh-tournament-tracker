from fastapi import FastAPI
from app.routers import players

app = FastAPI()

app.include_router(players.router, prefix="/players", tags=["players"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Yu-Gi-Oh! Tournament Tracker MVP"}