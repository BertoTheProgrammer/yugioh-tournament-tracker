from fastapi import FastAPI
from app.routers import players, tournament
import logging


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(tournament.router, prefix="/tournaments", tags=["tournaments"])

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI app starting up...")

@app.get("/")
async def root():
    return {"message": "Welcome to the Yu-Gi-Oh! Tournament Tracker MVP"}