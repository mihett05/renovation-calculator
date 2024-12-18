from adaptix.conversion import ConversionRetort

from domain.wall import Wall
from domain.floor import Floor

from .models import WallModel, FloorModel

retort = ConversionRetort()

wall_mapper = retort.get_converter(WallModel, Wall)
wall_model_mapper = retort.get_converter(Wall, WallModel)

floor_mapper = retort.get_converter(FloorModel, Floor)
floor_model_mapper = retort.get_converter(Floor, FloorModel)
