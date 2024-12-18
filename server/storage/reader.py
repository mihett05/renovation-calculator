from abc import ABCMeta, abstractmethod
from typing import Any

from domain.floor import Floor
from domain.wall import Wall


class Reader(metaclass=ABCMeta):
    @abstractmethod
    async def search_walls(self, search: str, limit: int) -> list[Wall]: ...

    @abstractmethod
    async def search_floors(self, search: str, limit: int) -> list[Floor]: ...

    @abstractmethod
    async def filter_walls(
        self, filters: dict[str, Any], page: int, page_size: int
    ) -> list[Wall]: ...

    @abstractmethod
    async def filter_floors(
        self, filters: dict[str, Any], page: int, page_size: int
    ) -> list[Floor]: ...
