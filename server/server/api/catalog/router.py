from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from storage.reader import Reader
from .models import WallsSearch, FloorsSearch

router = APIRouter(tags=["catalog"], route_class=DishkaRoute)


@router.get("/walls")
async def get_walls_catalog():
    pass


@router.get("/floors")
async def get_floors_catalog():
    pass


@router.get("/search/walls", response_model=WallsSearch)
async def search_walls(search: str, limit: int, reader: FromDishka[Reader]):
    return WallsSearch(walls=await reader.search_walls(search, limit))


@router.get("/search/floors", response_model=FloorsSearch)
async def search_floors(search: str, limit: int, reader: FromDishka[Reader]):
    return FloorsSearch(floors=await reader.search_floors(search, limit))
