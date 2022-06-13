from uuid import uuid4

from sqlalchemy import (Column, ForeignKey, Index, Integer, String, Table,
                        UniqueConstraint, Sequence)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from src.db.database import Base


routes_coordinates_table = Table(
    "routes_coordinates",
    Base.metadata,
    Column("route_id", ForeignKey("routes.id")),
    Column("coordinate_id", ForeignKey("coordinates.id")),
)


COORD_NUMBER_SEQ = Sequence('coordinates_number_seq') 


class Coordinates(Base):
    __tablename__ = "coordinates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)

    x_coord = Column(Integer, nullable=False)
    y_coord = Column(Integer, nullable=False)

    number = Column(Integer, COORD_NUMBER_SEQ, server_default=COORD_NUMBER_SEQ.next_value())

    __table_args__ = (
        UniqueConstraint("x_coord", "y_coord", name="chk_coordinates_x_coord_y_coord"),
        Index("idx_coordinates_x_coord_y_coord", "x_coord", "y_coord"),
    )


class Routes(Base):
    __tablename__ = "routes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_by_user_with_id = Column(Integer, nullable=False)
    coordinates = relationship(
        "Coordinates", secondary=routes_coordinates_table, backref="routes"
    )
    route_order = Column(ARRAY(UUID(as_uuid=True), as_tuple=True), nullable=False)
