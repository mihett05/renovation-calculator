from typing import Any

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, JSON
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(naming_convention=constraint_naming_conventions)
    type_annotation_map = {dict[str, Any]: JSON, dict[str, str]: JSON}


def get_engine(url: str) -> AsyncEngine:
    return create_async_engine(url, pool_size=16)


def get_session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)
