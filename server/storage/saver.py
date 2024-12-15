from abc import ABCMeta, abstractmethod

from domain.floor import Floor
from domain.wall import Wall


class Saver(metaclass=ABCMeta):
    @abstractmethod
    async def save_wall(self, wall: Wall): ...

    @abstractmethod
    async def save_floor(self, floor: Floor): ...
