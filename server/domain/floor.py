from dataclasses import dataclass
from enum import Enum


class FloorType(Enum):
    linoleum = "linoleum"
    laminate = "laminate"
    paint = "paint"
    ceramic = "ceramic"


@dataclass
class Floor:
    uid: str
    name: str
    url: str
    price: float  # стоимость за м^2
    floor_type: FloorType
    color: str
    photo: str
