import logging
import secrets
from functools import lru_cache
from typing import Any, Dict, List

from pydantic import BaseSettings, Field

logger = logging.getLogger(__name__)


class FastApiSettings(BaseSettings):
    debug: bool = False
    docs_url: str = "/pathfinder/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/pathfinder/openapi.json"
    redoc_url: str = "/pathfinder/redoc"
    title: str = "Pathfinder service"
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
    pg_database: str = Field(env="PG_DATABASE", default="pathfinder_db")

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


class RabbitMQSettings(BaseSettings):
    rabbitmq_host: str = Field(env="RABBITMQ_HOST", default="rabbitmq")
    rabbitmq_username: str = Field(env="RABBITMQ_USERNAME", default="user")
    rabbitmq_password: str = Field(env="RABBITMQ_PASSWORD", default="bitnami")
    rabbitmq_port: str = Field(env="RABBITMQ_PORT", default="5672")

    @property
    def rabbitmq_uri(self) -> str:
        return f"amqp://{self.rabbitmq_username}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}//"


class RedisSettings(BaseSettings):
    redis_host: str = Field(env="REDIS_HOST", default="redis")
    redis_username: str = Field(env="REDIS_USERNAME", default="")
    redis_password: str = Field(env="REDIS_PASSWORD", default="password123")
    redis_port: str = Field(env="REDIS_PORT", default="6379")

    redis_celery_db_index: str = Field(env="REDIS_CELERY_DB_INDEX", default="0")

    @property
    def _base_redis_uri(self) -> str:
        return f"redis://{self.redis_username}:{self.redis_password}@{self.redis_host}:{self.redis_port}"

    @property
    def redis_celery_uri(self) -> str:
        return f"{self._base_redis_uri}/{self.redis_celery_db_index}"


class UserServiceAPISettings(BaseSettings):
    user_service_host: str = Field(env="USER_SERVICE_HOST", default="user_service")
    user_service_port: int = Field(env="USER_SERVICE_PORT", default=3777)

    @property
    def user_service_url(self) -> str:
        return f"http://{self.user_service_host}:{str(self.user_service_port)}/api/v1"


class CelerySettings(RedisSettings, RabbitMQSettings):
    worker_name: str = "pathfinder_worker"
    celery_queue_name: str = "find-route-queue"


@lru_cache
def get_celery_settings() -> CelerySettings:
    logger.info("Loading config settings from the environment...")
    return CelerySettings()


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


@lru_cache
def get_user_service_settings() -> UserServiceAPISettings:
    return UserServiceAPISettings()
