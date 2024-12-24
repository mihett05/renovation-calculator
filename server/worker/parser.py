from abc import ABCMeta, abstractmethod

from aiohttp import ClientSession

from storage.saver import Saver


class Parser(metaclass=ABCMeta):
    saver: Saver
    session: ClientSession

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def prepare(self):
        """
        Метод для подготовки парсера к работе.
        Например, логин, добавление api-ключей и прочее
        """

    @abstractmethod
    async def parse_catalog(self):
        """
        Метод для парсинга и сохранения всего каталога сайта
        """
