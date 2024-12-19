from domain.filter import FloorsCriterias, WallsCriterias
from domain.floor import Floor
from domain.wall import Wall

from ..model import PydanticModel


class WallsSearch(PydanticModel):
    walls: list[Wall]


class FloorsSearch(PydanticModel):
    floors: list[Floor]


class WallsFilter(PydanticModel, WallsCriterias):
    pass


class FloorsFilter(PydanticModel, FloorsCriterias):
    pass
