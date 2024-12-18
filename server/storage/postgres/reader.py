from typing import Any

from sqlalchemy import select, ColumnElement, and_
from sqlalchemy.ext.asyncio import AsyncSession

from domain.floor import Floor
from domain.wall import Wall
from storage.reader import Reader


from .models import WallModel, FloorModel, Base
from .mappers import wall_mapper, floor_mapper


class PostgresReader(Reader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_walls(self, search: str, limit: int) -> list[Wall]:
        return [
            wall_mapper(wall)
            for wall in await self.session.scalars(
                select(WallModel)
                .where(
                    WallModel.name.ilike(f"%{search}%")
                    | WallModel.color.ilike(f"%{search}")
                )
                .order_by(WallModel.uid)
                .limit(limit)
            )
        ]

    async def search_floors(self, search: str, limit: int) -> list[Floor]:
        return [
            floor_mapper(floor)
            for floor in await self.session.scalars(
                select(FloorModel)
                .where(
                    FloorModel.name.ilike(f"%{search}%")
                    | FloorModel.color.ilike(f"%{search}")
                )
                .order_by(FloorModel.uid)
                .limit(limit)
            )
        ]

    async def filter_walls(
        self, filters: dict[str, Any], page: int, page_size: int
    ) -> list[Wall]:
        return [
            wall_mapper(wall)
            for wall in await self.session.scalars(
                select(WallModel)
                .where(and_(*self._filter_clauses(WallModel, filters)))
                .order_by(WallModel.uid)
                .limit(page_size)
                .offset(page * page_size)
            )
        ]

    async def filter_floors(
        self, filters: dict[str, Any], page: int, page_size: int
    ) -> list[Floor]:
        return [
            floor_mapper(floor)
            for floor in await self.session.scalars(
                select(FloorModel)
                .where(and_(*self._filter_clauses(FloorModel, filters)))
                .order_by(FloorModel.uid)
                .limit(page_size)
                .offset(page * page_size)
            )
        ]

    @staticmethod
    def _filter_clauses(
        model: type[Base], filters: dict[str, Any]
    ) -> list[ColumnElement[bool]]:
        return [
            getattr(model, field).__eq__(value)
            for field, value in filters.items()
            if hasattr(model, field)
        ]
