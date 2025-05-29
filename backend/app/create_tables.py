import asyncio
from app.database import Base, engine
import app.models.tournament
import app.models.player

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())
