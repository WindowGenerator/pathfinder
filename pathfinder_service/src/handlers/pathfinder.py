from fastapi import APIRouter, Depends, Query
from src.auth.check import JWTBearer
from src.worker.celery_api import CeleryApi
from src.worker.dependencies import get_celery_api

router = APIRouter()


@router.post(
    "/find_path", dependencies=[Depends(JWTBearer())], name="pathfinder:find-path"
)
async def find_path(
    from_point_id: str = Query(...),
    to_point_id: str = Query(...),
    celery_api: CeleryApi = Depends(get_celery_api),
):
    """
    Return coordinates by number_from and limit
    """

    task = celery_api.find_route(from_point_id, to_point_id)
    return {"task_id": task.id}
