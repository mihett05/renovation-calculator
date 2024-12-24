from bs4 import BeautifulSoup
from aiohttp import ClientSession


async def get_and_parse(session: ClientSession, url: str) -> BeautifulSoup:
    return BeautifulSoup(await (await session.get(url)).text(), features="lxml")
