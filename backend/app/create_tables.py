import asyncio
from app.database import Base, engine
import app.models.tournament
import app.models.player
import app.models.match

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())
