from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from storage.reader import Reader

from .models import FloorsFilter, FloorsSearch, WallsFilter, WallsSearch

router = APIRouter(tags=["catalog"], route_class=DishkaRoute)


@router.get("/walls", response_model=WallsSearch)
async def get_walls_catalog(
    data: Annotated[WallsFilter, Query()],
    reader: FromDishka[Reader],
):
    return WallsSearch(walls=await reader.filter_walls(data))


@router.get("/floors", response_model=FloorsSearch)
async def get_floors_catalog(
    data: Annotated[FloorsFilter, Query()],
    reader: FromDishka[Reader],
):
    return FloorsSearch(floors=await reader.filter_floors(data))


@router.get("/search/walls", response_model=WallsSearch)
async def search_walls(search: str, limit: int, reader: FromDishka[Reader]):
    return WallsSearch(walls=await reader.search_walls(search, limit))


@router.get("/search/floors", response_model=FloorsSearch)
async def search_floors(search: str, limit: int, reader: FromDishka[Reader]):
    return FloorsSearch(floors=await reader.search_floors(search, limit))
