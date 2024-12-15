from domain.floor import Floor
from domain.wall import Wall
from storage.saver import Saver


class MockSaver(Saver):
    def __init__(self, storage: list[Wall | Floor]):
        self.storage = storage

    async def save_wall(self, wall: Wall):
        self.storage.append(wall)

    async def save_floor(self, floor: Floor):
        self.storage.append(floor)
