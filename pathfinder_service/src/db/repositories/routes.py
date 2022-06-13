import logging
import math
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models import Routes
from src.db.repositories.coordinates import CoordinatesRepository
from src.schemas.coordinates import Coordinate as CoordinateSchema
from src.schemas.coordinates import CoordinateID as CoordinateIDSchema
from src.schemas.routes import ReportPerUser as ReportPerUserSchema
from src.schemas.routes import Route as RouteSchema

logger = logging.getLogger(__name__)

XCoord = YCoord = int
Point = Tuple[XCoord, YCoord]


class RoutesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self._coord_repo = CoordinatesRepository(self._session)

    async def get_routes(self) -> List[RouteSchema]:
        result = await self._session.execute(
            select(Routes).options(selectinload(Routes.coordinates))
        )
        routes = []

        for route in result.scalars():
            routes.append(self._convert_route_from_db(route))

        return routes

    async def save_route(
        self,
        route_id: str,
        created_by_user_with_id: int,
        coordinate_ids: List[CoordinateIDSchema],
    ) -> RouteSchema:
        route = Routes(
            id=route_id,
            created_by_user_with_id=created_by_user_with_id,
            coordinates=await self._coord_repo.get_raw_coordinates_by_ids(
                coordinate_ids
            ),
            route_order=coordinate_ids,  # rename to route_order
        )
        await self._session.commit()

        async with self._session.begin():
            self._session.add(route)

        return await self.get_route_by_id(route_id)

    async def get_route_by_id(self, route_id: str) -> Optional[RouteSchema]:
        result = await self._session.execute(
            select(Routes)
            .where(Routes.id == route_id)
            .options(selectinload(Routes.coordinates))
        )
        await self._session.commit()
        route = result.scalar()

        if route is None:
            return None

        return self._convert_route_from_db(route)

    def _convert_route_from_db(self, route) -> RouteSchema:
        coordinates = {}

        for coord in route.coordinates:
            coordinates[str(coord.id)] = CoordinateSchema(
                id=str(coord.id),
                name=coord.name,
                x_coord=coord.x_coord,
                y_coord=coord.y_coord,
            )

        return RouteSchema(
            id=str(route.id),
            created_by_user_with_id=route.created_by_user_with_id,
            coordinates=[
                coordinates[str(route_coord_id)] for route_coord_id in route.route_order
            ],
        )

    async def get_reports(self) -> List[ReportPerUserSchema]:
        routes: List[RouteSchema] = await self.get_routes()

        user_to_report = {}

        for route in routes:
            if route.created_by_user_with_id not in user_to_report:
                user_to_report[route.created_by_user_with_id] = {
                    "routes_count": 0,
                    "routes_length": 0,
                }

            user_to_report[route.created_by_user_with_id]["routes_count"] += 1

            route_length = 0

            previous_coord = None

            for coord in route.coordinates:
                if previous_coord is None:
                    previous_coord = coord
                    continue

                route_length += math.sqrt(
                    (previous_coord.x_coord - coord.x_coord) ** 2
                    + (previous_coord.y_coord - coord.y_coord) ** 2
                )

                previous_coord = coord

            user_to_report[route.created_by_user_with_id][
                "routes_length"
            ] += route_length

        reports = []

        for user_id, report in user_to_report.items():
            reports.append(
                ReportPerUserSchema(
                    created_by_user_with_id=user_id,
                    routes_count=report["routes_count"],
                    routes_length=report["routes_length"],
                )
            )

        return reports
