import logging

from celery import Celery, Task
from celery.result import AsyncResult
from src.settings import CelerySettings, get_celery_settings

logger = logging.getLogger(__name__)
settings = get_celery_settings()


class CeleryApi:
    def __init__(self, settings: CelerySettings) -> None:
        self._app = Celery(
            settings.worker_name,
            backend=settings.redis_celery_uri,
            broker=settings.rabbitmq_uri,
        )

        self._app.conf.task_default_queue = settings.celery_queue_name

    def find_route(self, from_point_id: str, to_point_id: str) -> Task:
        return self._app.send_task(
            "find_route",
            kwargs={"from_point_id": from_point_id, "to_point_id": to_point_id},
        )

    def get_task(self, task_id: str) -> Task:
        return AsyncResult(task_id)
