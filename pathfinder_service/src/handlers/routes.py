import json
import logging
from typing import List

from celery.states import READY_STATES, SUCCESS
from fastapi import (APIRouter, Body, Depends, HTTPException, Query, Request,
                     status)
from src.apis.users_api import UsersApi
from src.auth.check import JWTBearer
from src.db.dependencies import get_routes_repository
from src.db.repositories.routes import RoutesRepository
from src.schemas.coordinates import Coordinate, CoordinateIDs
from src.schemas.routes import ReportPerUser, Route
from src.worker.celery_api import CeleryApi
from src.worker.dependencies import get_celery_api

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/routes")


@router.post(
    "/save",
    dependencies=[Depends(JWTBearer())],
    response_model=Route,
    status_code=status.HTTP_200_OK,
    name="routes:save-route",
)
async def save_route(
    request: Request,
    route_id: str = Query(...),
    body: CoordinateIDs = Body(...),
    routes_repository: RoutesRepository = Depends(get_routes_repository),
    users_api: UsersApi = Depends(UsersApi),
) -> Route:
    """
    Save route for current user
    """

    current_user = await users_api.get_current_user(request)

    return await routes_repository.save_route(
        route_id, current_user["id"], body.coordinate_ids
    )


@router.get(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_model=List[Route],
    status_code=status.HTTP_200_OK,
    name="routes:get-routes",
)
async def get_all_routes(
    routes_repository: RoutesRepository = Depends(get_routes_repository),
) -> List[Route]:
    """
    Get all routes
    """

    return await routes_repository.get_routes()


@router.get(
    "/report",
    dependencies=[Depends(JWTBearer())],
    response_model=List[ReportPerUser],
    status_code=status.HTTP_200_OK,
    name="routes:get-report",
)
async def get_report(
    routes_repository: RoutesRepository = Depends(get_routes_repository),
) -> List[ReportPerUser]:
    """
    Create and get report by users and their routes
    """

    return await routes_repository.get_reports()


@router.get(
    "/route",
    dependencies=[Depends(JWTBearer())],
    response_model=Route,
    status_code=status.HTTP_200_OK,
    name="routes:get-route",
)
async def get_route(
    route_id: str,
    celery_api: CeleryApi = Depends(get_celery_api),
    routes_repository: RoutesRepository = Depends(get_routes_repository),
) -> Route:
    """
    Get route by id
    """

    route = await routes_repository.get_route_by_id(route_id)

    if route is not None:
        return route

    task = celery_api.get_task(route_id)

    route = Route(
        id=route_id,
        coordinates=[],
    )

    if task.state not in READY_STATES:
        return route

    if task.state == SUCCESS:
        route.coordinates = [
            Coordinate(
                id=coord["id"],
                name=coord["name"],
                x_coord=coord["x_coord"],
                y_coord=coord["y_coord"],
            )
            for coord in task.result["coordinates"]
        ]
    else:
        raise HTTPException(status_code=400, detail=json.dumps(task.result))

    return route
