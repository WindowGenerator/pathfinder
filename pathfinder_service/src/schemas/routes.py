from typing import List

from pydantic import BaseModel, Field
from src.schemas.coordinates import Coordinate


class Route(BaseModel):
    id: str = Field(...)
    created_by_user_with_id: int = Field(default=None)
    coordinates: List[Coordinate] = Field(...)


class ReportPerUser(BaseModel):
    created_by_user_with_id: int = Field(...)
    routes_count: int = Field(...)
    routes_length: float = Field(...)
