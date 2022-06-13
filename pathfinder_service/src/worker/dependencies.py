from fastapi import Depends, Request
from src.settings import CelerySettings, get_celery_settings
from src.worker.celery_api import CeleryApi


async def get_celery_api(
    request: Request, celery_settings: CelerySettings = Depends(get_celery_settings)
) -> CeleryApi:
    return CeleryApi(celery_settings)
