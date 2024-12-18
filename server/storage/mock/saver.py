from domain.floor import Floor
from domain.wall import Wall
from storage.saver import Saver


class MockSaver(Saver):
    def __init__(self, storage: list[Wall | Floor]):
        self.storage = storage

    async def save_walls(self, walls: list[Wall]):
        self.storage += walls

    async def save_floors(self, floors: list[Floor]):
        self.storage += floors
