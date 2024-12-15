from abc import ABCMeta, abstractmethod

from storage.saver import Saver


class Parser(metaclass=ABCMeta):
    saver: Saver

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

    @abstractmethod
    async def find(self, search: str):
        """
        Метод для поиска элементов по пользовательскому вводу
        """
