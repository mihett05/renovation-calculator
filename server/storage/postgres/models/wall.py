from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

from domain.wall import WallType
from .base import Base


class WallModel(Base):
    __tablename__ = "walls"

    uid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    url: Mapped[str]
    price: Mapped[float]
    wall_type: Mapped[WallType] = mapped_column(Enum(WallType))
    color: Mapped[str]
    photo: Mapped[str]
