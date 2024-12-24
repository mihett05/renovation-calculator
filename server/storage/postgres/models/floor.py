from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

from domain.floor import FloorType
from .base import Base


class FloorModel(Base):
    __tablename__ = "floors"

    uid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    url: Mapped[str]
    price: Mapped[float]
    floor_type: Mapped[FloorType] = mapped_column(Enum(FloorType))
    color: Mapped[str]
    photo: Mapped[str]
