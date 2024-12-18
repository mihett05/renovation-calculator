from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from dataclasses import asdict

from domain.floor import Floor
from domain.wall import Wall
from storage.postgres.models import WallModel, FloorModel
from storage.saver import Saver


class PostgresSaver(Saver):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_walls(self, walls: list[Wall]):
        insert_stmt = insert(WallModel).values([asdict(wall) for wall in walls])
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["uid"],
            set_={
                "url": insert_stmt.excluded.url,
                "price": insert_stmt.excluded.price,
                "wall_type": insert_stmt.excluded.wall_type,
                "color": insert_stmt.excluded.color,
                "photo": insert_stmt.excluded.photo,
            },
        )
        await self.session.execute(upsert_stmt)
        await self.session.commit()

    async def save_floors(self, floors: list[Floor]):
        insert_stmt = insert(FloorModel).values([asdict(floor) for floor in floors])
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["uid"],
            set_={
                "url": insert_stmt.excluded.url,
                "price": insert_stmt.excluded.price,
                "floor_type": insert_stmt.excluded.floor_type,
                "color": insert_stmt.excluded.color,
                "photo": insert_stmt.excluded.photo,
            },
        )
        await self.session.execute(insert_stmt)
        await self.session.commit()
