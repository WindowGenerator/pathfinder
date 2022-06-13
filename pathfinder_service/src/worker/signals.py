import asyncio
from dataclasses import dataclass

from celery.signals import worker_process_init, worker_process_shutdown
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from src.db.database import async_session
from src.settings import get_postgres_settings


@dataclass
class ClobalStore:
    session: AsyncSession = None
    engine: AsyncEngine = None


GLOBAL_STORE = ClobalStore()


@worker_process_init.connect
def init(*args, **kwargs) -> None:
    global GLOBAL_STORE
    postgres_settings = get_postgres_settings()

    loop = asyncio.get_event_loop()
    _async_session, engine = loop.run_until_complete(
        async_session(postgres_settings.asyncpg_url)
    )

    GLOBAL_STORE.engine = engine
    GLOBAL_STORE.session = _async_session


@worker_process_shutdown.connect
def shutdown(*args, **kwargs) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(GLOBAL_STORE.engine.dispose())
