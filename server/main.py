import asyncio

from worker.sites.ekonomstroy.parser import EkonomstroyParser
from storage.mock.saver import MockSaver


async def main():
    storage = []
    saver = MockSaver(storage)
    async with EkonomstroyParser(saver) as parser:
        await parser.parse_catalog()
    print(len(saver.storage))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
