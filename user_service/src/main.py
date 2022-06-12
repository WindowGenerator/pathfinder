from typing import Callable

from fastapi import FastAPI
from src.db.events import close_db_connection, connect_to_db
from src.handlers import router as api_router
from src.settings import (get_app_settings, get_fastapi_settings,
                          get_postgres_settings)
from starlette.middleware.cors import CORSMiddleware


def _create_start_app_handler(
    app: FastAPI,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        postgres_settings = get_postgres_settings()
        await connect_to_db(app, postgres_settings.asyncpg_url)

    return start_app


def _create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app


def create_app() -> FastAPI:
    app_settings = get_app_settings()
    fastapi_settings = get_fastapi_settings()

    app = FastAPI(**fastapi_settings.fastapi_init_args)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=app_settings.api_prefix)

    app.add_event_handler(
        "startup",
        _create_start_app_handler(app),
    )
    app.add_event_handler(
        "shutdown",
        _create_stop_app_handler(app),
    )

    return app
