from typing import List

from fastapi import APIRouter, Depends, Query
from src.auth.check import JWTBearer
from src.db.dependencies import get_coordinates_repository
from src.db.repositories.coordinates import CoordinatesRepository
from src.schemas.coordinates import Coordinate

router = APIRouter()


@router.get(
    "/coordinates",
    dependencies=[Depends(JWTBearer())],
    response_model=List[Coordinate],
    name="coordinates:get-coordinates",
)
async def coordinates(
    number_from: int = Query(...),
    limit: int = Query(default=1000),
    coordinates_repository: CoordinatesRepository = Depends(get_coordinates_repository),
) -> List[Coordinate]:
    """
    Return coordinates by number_from and limit
    """

    coordinates: List[Coordinate] = await coordinates_repository.get_coordinates(
        number_from, limit=limit
    )

    return coordinates
