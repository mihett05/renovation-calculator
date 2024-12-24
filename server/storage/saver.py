from abc import ABCMeta, abstractmethod

from domain.floor import Floor
from domain.wall import Wall


class Saver(metaclass=ABCMeta):
    @abstractmethod
    async def save_walls(self, walls: list[Wall]): ...

    @abstractmethod
    async def save_floors(self, floors: list[Floor]): ...
