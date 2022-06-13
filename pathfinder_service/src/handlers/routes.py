from typing import List

from fastapi import APIRouter, Depends, Body, Query
from src.db.dependencies import get_routes_repository
from src.db.repositories.routes import RoutesRepository
from src.schemas.coordinates import CoordinateID
from src.schemas.routes import Route, ReportPerUser
from src.auth.check import JWTBearer


router = APIRouter(prefix="/routes")


@router.post("/save", dependencies=[Depends(JWTBearer())], response_model=Route, name="routes:save-route")
async def save_route(
    user_id: int = Query(...),
    coordinate_ids: List[CoordinateID] = Body(...),
    routes_repository: RoutesRepository = Depends(get_routes_repository),
) -> Route:
    """
    Return coordinates by number_from and limit
    """

    return await routes_repository.save_route(user_id, coordinate_ids)


@router.get("/", dependencies=[Depends(JWTBearer())], response_model=List[Route], name="routes:get-routes")
async def get_all_routes(
    routes_repository: RoutesRepository = Depends(get_routes_repository),
) -> List[Route]:
    """
    Return coordinates by number_from and limit
    """

    return await routes_repository.get_routes()


@router.get("/report", dependencies=[Depends(JWTBearer())], response_model=List[ReportPerUser], name="routes:get-report")
async def get_report(
    routes_repository: RoutesRepository = Depends(get_routes_repository),
) -> List[ReportPerUser]:
    """
    Return coordinates by number_from and limit
    """

    return await routes_repository.get_reports()