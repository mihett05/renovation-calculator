from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from settings import Settings
from .models.base import get_engine, get_session_maker

from storage.saver import Saver
from storage.reader import Reader
from .reader import PostgresReader
from .saver import PostgresSaver


class PostgresProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def engine(self, settings: Settings) -> AsyncEngine:
        return get_engine(str(settings.postgres_url))

    @provide(scope=Scope.APP)
    def session_maker(self, engine: AsyncEngine) -> async_sessionmaker:
        return get_session_maker(engine)

    @provide()
    async def session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    reader = provide(source=PostgresReader, provides=Reader)
    saver = provide(source=PostgresSaver, provides=Saver)
