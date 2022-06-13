import logging
import random
from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.coordinates import CoordinatesRepository
from src.schemas.coordinates import Coordinate as CoordinateSchema

logger = logging.getLogger(__name__)

XCoord = YCoord = int
Point = Tuple[XCoord, YCoord]


class PathfinderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._coord_repo = CoordinatesRepository(self._session)

    async def find_route_by_points(
        self, from_point_id: str, to_point_id: str
    ) -> List[CoordinateSchema]:
        from_point = await self._coord_repo.get_coordinate_by_id(from_point_id)
        to_point = await self._coord_repo.get_coordinate_by_id(to_point_id)

        route_length = random.randint(0, 98)

        points = []

        if route_length != 0:
            table_length = await self._coord_repo.get_length()
            points = await self._coord_repo.get_coordinates(
                number_from=random.randint(route_length, table_length - route_length),
                limit=route_length,
            )

        points.insert(0, from_point)
        points.append(to_point)

        return points
