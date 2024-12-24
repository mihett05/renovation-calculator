from sqlalchemy import ColumnElement, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.filter import FilterCriterias, FloorsCriterias, WallsCriterias
from domain.floor import Floor
from domain.wall import Wall
from storage.reader import Reader

from .mappers import floor_mapper, wall_mapper
from .models import Base, FloorModel, WallModel


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

    async def filter_walls(self, filters: WallsCriterias) -> list[Wall]:
        clauses = self._filter_clauses(WallModel, filters)
        if filters.wall_type:
            clauses.append(WallModel.wall_type == filters.wall_type.value)

        return [
            wall_mapper(wall)
            for wall in await self.session.scalars(
                select(WallModel)
                .where(and_(*clauses))
                .order_by(WallModel.uid)
                .limit(filters.page_size)
                .offset(filters.page * filters.page_size)
            )
        ]

    async def filter_floors(self, filters: FloorsCriterias) -> list[Floor]:
        clauses = self._filter_clauses(FloorModel, filters)
        if filters.floor_type:
            clauses.append(FloorModel.floor_type == filters.floor_type.value)
        return [
            floor_mapper(floor)
            for floor in await self.session.scalars(
                select(FloorModel)
                .where(and_(*clauses))
                .order_by(FloorModel.uid)
                .limit(filters.page_size)
                .offset(filters.page * filters.page_size)
            )
        ]

    @staticmethod
    def _filter_clauses(
        model: type[Base], filters: FilterCriterias
    ) -> list[ColumnElement[bool]]:
        clauses = []
        if filters.name:
            clauses.append(model.name.ilike(f"%{filters.name}%"))
        if filters.color:
            clauses.append(model.color.ilike(f"%{filters.color}%"))
        if filters.price_min:
            clauses.append(model.price >= filters.price_min)
        if filters.price_max:
            clauses.append(model.price <= filters.price_max)
        return clauses
