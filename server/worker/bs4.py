from bs4 import BeautifulSoup
from aiohttp import ClientSession


async def get_and_parse(session: ClientSession, url: str) -> BeautifulSoup:
    BeautifulSoup(await (await session.get(url)).text(), parser="lxml")
