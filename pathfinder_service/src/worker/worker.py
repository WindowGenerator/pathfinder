import asyncio
import logging
from typing import Any, Dict, List

from celery import Celery
from src.db.repositories.pathfinder import PathfinderRepository
from src.settings import get_celery_settings, get_postgres_settings
from src.worker.signals import GLOBAL_STORE

logger = logging.getLogger(__name__)
celery_settings = get_celery_settings()
postgres_settings = get_postgres_settings()


app = Celery(
    celery_settings.worker_name,
    backend=celery_settings.redis_celery_uri,
    broker=celery_settings.rabbitmq_uri,
)

app.conf.task_routes = {"find_route": {"queue": celery_settings.celery_queue_name}}

app.conf.update(task_track_started=True)


async def _find_route(from_point_id: str, to_point_id: str) -> List[Dict]:
    logger.error(GLOBAL_STORE)
    async with GLOBAL_STORE.session() as session:
        pathfinder_repo = PathfinderRepository(session)

        return [
            coord.dict()
            for coord in await pathfinder_repo.find_route_by_points(
                from_point_id, to_point_id
            )
        ]


@app.task(acks_late=True, name="find_route", bind=True)
def find_route(self, from_point_id: str, to_point_id: str) -> Dict[str, Any]:
    loop = asyncio.get_event_loop()
    return {
        "coordinates": loop.run_until_complete(_find_route(from_point_id, to_point_id))
    }
