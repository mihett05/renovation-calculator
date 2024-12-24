from dataclasses import dataclass

from domain.floor import FloorType
from domain.wall import WallType


@dataclass
class FilterCriterias:
    name: str | None = None
    color: str | None = None
    price_min: int | None = None
    price_max: int | None = None


class WallsCriterias(FilterCriterias):
    wall_type: WallType | None = None
    page: int
    page_size: int


class FloorsCriterias(FilterCriterias):
    floor_type: FloorType | None = None
    page: int
    page_size: int
