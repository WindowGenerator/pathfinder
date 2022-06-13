from fastapi import APIRouter
from src.handlers import coordinates, pathfinder, routes

router = APIRouter(prefix="/pathfinder")

router.include_router(coordinates.router, tags=["coordinates"])
router.include_router(pathfinder.router, tags=["pathfinder"])
router.include_router(routes.router, tags=["routes"])
