from dataclasses import dataclass
from enum import Enum


class WallType(Enum):
    wallpaper = "wallpaper"
    paint = "paint"
    ceramic = "ceramic"


@dataclass
class Wall:
    uid: str
    url: str
    price: float  # стоимость за м^2
    wall_type: WallType
    color: str
    photo: str
