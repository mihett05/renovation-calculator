import asyncio
from typing import Callable, Coroutine, Any
from dataclasses import dataclass

from bs4 import BeautifulSoup
from aiohttp import ClientSession

from domain.floor import Floor
from domain.wall import Wall, WallType
from storage.saver import Saver
from worker.parser import Parser
from worker.bs4 import get_and_parse


@dataclass
class Page:
    uid: str
    url: str
    price: int
    unit: str
    photo: str | None
    description: dict[str, str]


class EkonomstroyParser(Parser):
    def __init__(self, saver: Saver):
        self.saver = saver
        self.session = ClientSession()

    async def find(self, search: str):
        pass

    async def parse_catalog(self):
        pass

    async def parse_walls(self):
        (
            self.fetch_items(
                "https://www.ekonomstroy.ru/catalog/oboi_pod_pokrasku/",
                self.parse_walls_wallpapers_fabric,
            ),
            self.fetch_items(
                "https://www.ekonomstroy.ru/catalog/steklokholst/",
                self.parse_walls_wallpapers_fiberglass,
            ),
            self.fetch_items(
                "https://www.ekonomstroy.ru/catalog/plenka_samokleyushchayasya/",
                self.parse_walls_wallpapers_fiberglass,
            ),
            self.fetch_items(
                "https://www.ekonomstroy.ru/catalog/plitka_keramicheskaya_keramogranit/",
                self.parse_walls_wallpapers_fiberglass,
            ),
            self.fetch_items(
                "https://www.ekonomstroy.ru/catalog/dlya_sten_i_potolkov/",
                self.parse_walls_wallpapers_fiberglass,
            ),
        )

    async def parse_walls_wallpapers_fabric(
        self, page: Page, soup: BeautifulSoup
    ) -> Wall | None:
        price = page.price
        if page.unit == "рул" and "размер" in page.description:
            height, width = map(
                float,
                page.description["размер"]
                .replace(" ", "")
                .replace(",", ".")[:-1]
                .split("x"),
            )
            price = page.price / (height * width)
        elif page.unit != "м2":
            return

        return Wall(
            uid=page.uid,
            url=page.url,
            price=price,
            photo=page.photo,
            wall_type=WallType.wallpaper,
            color=page.description["цвет"],
        )

    async def parse_walls_wallpapers_fiberglass(
        self, page: Page, soup: BeautifulSoup
    ) -> Wall | None:
        price = page.price
        if (
            page.unit == "шт"
            and "длина" in page.description
            and "ширина" in page.description
        ):
            height = float(page.description["ширина"].replace(" ", "")[:-2]) / 1000
            width = float(page.description["длина"].replace(" ", "")[:-1])
            price = page.price / (height * width)
        elif page.unit != "м2":
            return

        return Wall(
            uid=page.uid,
            url=page.url,
            price=price,
            photo=page.photo,
            wall_type=WallType.wallpaper,
            color=page.description["цвет"],
        )

    async def parse_walls_wallpapers_wrap(
        self, page: Page, soup: BeautifulSoup
    ) -> Wall | None:
        price = page.price
        if (
            page.unit == "шт"
            and "длина" in page.description
            and "ширина" in page.description
        ):
            height = float(
                page.description["ширина"].replace(" ", "").replace(",", ".")[:-1]
            )
            width = float(page.description["длина"].replace(" ", "")[:-1])
            price = page.price / (height * width)
        elif page.unit != "м2":
            return

        return Wall(
            uid=page.uid,
            url=page.url,
            price=price,
            photo=page.photo,
            wall_type=WallType.wallpaper,
            color=page.description["цвет"],
        )

    async def parse_walls_ceramic(self, page: Page, soup: BeautifulSoup) -> Wall:
        return Wall(
            uid=page.uid,
            url=page.url,
            price=page.price,
            photo=page.photo,
            wall_type=WallType.ceramic,
            color=page.description["цвет"],
        )

    async def parse_walls_paint(self, page: Page, soup: BeautifulSoup) -> Wall:
        if (
            page.unit == "шт"
            and "расход" in page.description
            and ("объем" in page.description or "фасовка" in page.description)
        ):
            usage = (
                page.description["расход"].replace(" ", "")[:-2]
                if "расход" in page.description
                else page.description["фасовка"].replace(" ", "")[:-2]
            ).replace(",", ".")
            return Wall(
                uid=page.uid,
                url=page.url,
                price=page.price,
                photo=page.photo,
                wall_type=WallType.ceramic,
                color=page.description["цвет"],
            )

    async def fetch_items(
        self,
        catalog: str,
        parse: Callable[
            [Page, BeautifulSoup], Coroutine[Any, Any, Wall | Floor | None]
        ],
    ):
        soup = await get_and_parse(
            self.session,
            f"{catalog}?pagecount=4096",
        )
        links = [
            f"https://www.ekonomstroy.ru{link.get('href')}"
            for link in soup.select(".asd2 .asd1 a.bx_catalog_item_images[href]")
        ]
        await asyncio.gather(*[self.fetch_wrapper(parse, link) for link in links])

    async def fetch_wrapper(
        self,
        parse: Callable[
            [Page, BeautifulSoup], Coroutine[Any, Any, Wall | Floor | None]
        ],
        url: str,
    ):
        soup = await get_and_parse(self.session, url)

        photo = None
        if a_img := soup.select_one(".detail-img-zoom[href]"):
            photo = a_img.get("href")

        description = {}
        if rows := soup.select_one(".descr dl.row"):
            for row in rows:
                if key := row.select_one("dt"):
                    if value := row.select_one("dd"):
                        description[key.text.lower()] = value.text

        price = None
        unit = None
        if price_span := soup.select_one(".price_in_int > span.span_price"):
            price, unit = self.parse_price(price_span.text)

        uid = None
        if uid_span := soup.select_one(".attrs p span.att_span"):
            uid = uid_span.text.strip()

        if price and unit and uid:
            result = await parse(
                Page(
                    uid=uid,
                    url=url,
                    price=price,
                    unit=unit,
                    photo=photo,
                    description=description,
                ),
                soup,
            )
        # нет смысла парсить покрытия без цены

    @staticmethod
    def parse_price(price: str) -> tuple[int, str]:
        """
        Парсит цену с сайта и возвращает цену и единицу измерения (шт, м2, ...)
        """
        price_part, unit_part = price.split("/")
        return int("".join(filter(str.isdigit, price_part))), unit_part.lower()
