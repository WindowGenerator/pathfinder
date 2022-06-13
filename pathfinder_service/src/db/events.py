import logging

from fastapi import FastAPI
from src.db.database import async_session

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI, asyncpg_url: str) -> None:
    logger.info(f"Connecting to {asyncpg_url}")

    app.state.db, app.state.engine = await async_session(asyncpg_url)

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.engine.dispose()

    logger.info("Connection closed")
