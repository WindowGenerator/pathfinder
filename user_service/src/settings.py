import logging
import secrets
from functools import lru_cache
from typing import Any, Dict, List

from pydantic import BaseSettings, Field

logger = logging.getLogger(__name__)


class FastApiSettings(BaseSettings):
    debug: bool = False
    docs_url: str = "/users/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/users/openapi.json"
    redoc_url: str = "/users/redoc"
    title: str = "Users service"
    version: str = "0.0.1"

    @property
    def fastapi_init_args(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }


class PostgresSettings(BaseSettings):
    pg_user: str = Field(env="PG_USER", default="postgres")
    pg_pass: str = Field(env="PG_PASSWORD", default="secret")
    pg_host: str = Field(env="PG_HOST", default="postgres")
    pg_database: str = Field(env="PG_DATABASE", default="users_db")

    @property
    def asyncpg_url(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_pass}@{self.pg_host}:5432/{self.pg_database}"

    min_connection_count: int = 1
    max_connection_count: int = 10


class AppSettings(BaseSettings):
    api_prefix: str = "/api/v1"

    jwt_secret: str = secrets.token_hex(16)
    jwt_algorithm: str = "HS256"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO

    class Config:
        validate_assignment = True


@lru_cache
def get_app_settings() -> AppSettings:
    logger.info("Loading config settings from the environment...")
    return AppSettings()


@lru_cache
def get_fastapi_settings() -> FastApiSettings:
    logger.info("Loading config settings from the environment...")
    return FastApiSettings()


@lru_cache
def get_postgres_settings() -> PostgresSettings:
    logger.info("Loading config settings from the environment...")
    return PostgresSettings()
