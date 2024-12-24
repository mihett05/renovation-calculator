import asyncio
from typing import Callable, Coroutine, Any
from dataclasses import dataclass

from bs4 import BeautifulSoup
from aiohttp import ClientSession

from domain.floor import Floor, FloorType
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
    photo: str
    description: dict[str, str]
    name: str


class EkonomstroyParser(Parser):
    def __init__(self, saver: Saver):
        self.saver = saver
        self.session = ClientSession()

    async def parse_catalog(self):
        walls, floors = await asyncio.gather(*(self.parse_walls(), self.parse_floors()))
        await self.saver.save_walls(walls)
        await self.saver.save_floors(floors)

    async def parse_walls(self) -> list[Wall]:
        return [
            wall
            for result in await asyncio.gather(
                *(
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
                        self.parse_walls_wallpapers_wrap,
                    ),
                    self.fetch_items(
                        "https://www.ekonomstroy.ru/catalog/plitka_keramicheskaya_keramogranit/",
                        self.parse_walls_ceramic,
                    ),
                    self.fetch_items(
                        "https://www.ekonomstroy.ru/catalog/dlya_sten_i_potolkov/",
                        self.parse_walls_paint,
                    ),
                )
            )
            for wall in result
        ]

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
            name=page.name,
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
            height = self.parse_as_float(page.description["ширина"]) / (
                1000 if "мм" in page.description["ширина"] else 1
            )
            width = self.parse_as_float(page.description["длина"]) / (
                1000 if "мм" in page.description["длина"] else 1
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
            name=page.name,
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
            width = float(
                page.description["длина"].replace(" ", "").replace(",", ".")[:-1]
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
            name=page.name,
        )

    async def parse_walls_ceramic(self, page: Page, soup: BeautifulSoup) -> Wall:
        return Wall(
            uid=page.uid,
            url=page.url,
            price=page.price,
            photo=page.photo,
            wall_type=WallType.ceramic,
            color=page.description["цвет"],
            name=page.name,
        )

    async def parse_walls_paint(self, page: Page, soup: BeautifulSoup) -> Wall | None:
        if (
            page.unit == "шт"
            and "расход" in page.description
            and ("объем" in page.description or "фасовка" in page.description)
        ):
            usage = self.parse_as_float(page.description["расход"].split("-")[-1])
            volume = self.parse_as_float(
                page.description["объем"]
                if "объем" in page.description
                else page.description["фасовка"]
            )

            return Wall(
                uid=page.uid,
                url=page.url,
                price=page.price * volume / (usage / 1000),
                photo=page.photo,
                wall_type=WallType.paint,
                color=page.description["цвет"],
                name=page.name,
            )

    async def parse_floors(self) -> list[Floor]:
        return [
            floor
            for result in await asyncio.gather(
                *(
                    self.fetch_items(
                        "https://www.ekonomstroy.ru/catalog/plitka_keramicheskaya_keramogranit/",
                        self.parse_floors_ceramic,
                    ),
                    self.fetch_items(
                        "https://www.ekonomstroy.ru/catalog/napolnye_pokrytiya/",
                        self.parse_floors_paint,
                    ),
                    self.fetch_items(
                        "https://www.ekonomstroy.ru/catalog/laminat/",
                        self.parse_floor_laminate,
                    ),
                    self.fetch_items(
                        "https://www.ekonomstroy.ru/catalog/linoleum/",
                        self.parse_floor_linoleum,
                    ),
                )
            )
            for floor in result
        ]

    async def parse_floors_ceramic(self, page: Page, soup: BeautifulSoup) -> Floor:
        return Floor(
            uid=page.uid,
            url=page.url,
            price=page.price,
            photo=page.photo,
            floor_type=FloorType.ceramic,
            color=page.description["цвет"],
            name=page.name,
        )

    async def parse_floors_paint(self, page: Page, soup: BeautifulSoup) -> Floor | None:
        if (
            page.unit == "шт"
            and "расход" in page.description
            and ("объем" in page.description or "фасовка" in page.description)
        ):
            if "кг" in page.description["расход"]:
                mass, area = page.description["расход"].split("/")
                mass = self.parse_as_float(mass)
                area = self.parse_as_float(area.split("-")[-1])
                usage = mass / area
            else:
                usage = (
                    self.parse_as_float(page.description["расход"].split("-")[-1])
                    / 1000
                )
            volume = self.parse_as_float(
                page.description["объем"] if "объем" else page.description["фасовка"]
            )

            return Floor(
                uid=page.uid,
                url=page.url,
                price=page.price * volume / usage,
                photo=page.photo,
                floor_type=FloorType.paint,
                color=page.description["цвет"],
                name=page.name,
            )

    async def parse_floor_laminate(
        self, page: Page, soup: BeautifulSoup
    ) -> Floor | None:
        return Floor(
            uid=page.uid,
            url=page.url,
            price=page.price,
            photo=page.photo,
            floor_type=FloorType.laminate,
            color=page.description["цвет"],
            name=page.name,
        )

    async def parse_floor_linoleum(
        self, page: Page, soup: BeautifulSoup
    ) -> Floor | None:
        return Floor(
            uid=page.uid,
            url=page.url,
            price=page.price,
            photo=page.photo,
            floor_type=FloorType.linoleum,
            color=page.description["цвет"],
            name=page.name,
        )

    async def fetch_items(
        self,
        catalog: str,
        parse: Callable[
            [Page, BeautifulSoup], Coroutine[Any, Any, Wall | Floor | None]
        ],
    ) -> list[Wall | Floor]:
        soup = await get_and_parse(
            self.session,
            f"{catalog}?pagecount=4096",
        )
        links = [
            f"https://www.ekonomstroy.ru{link.get('href')}"
            for link in soup.select(".asd2 .asd1 a.bx_catalog_item_images[href]")
        ]
        return [
            result
            for result in await asyncio.gather(
                *[self.fetch_wrapper(parse, link) for link in links]
            )
            if result
        ]

    async def fetch_wrapper(
        self,
        parse: Callable[
            [Page, BeautifulSoup], Coroutine[Any, Any, Wall | Floor | None]
        ],
        url: str,
    ) -> Wall | Floor | None:
        soup = await get_and_parse(self.session, url)

        name = None
        if h1 := soup.select_one(".bx-title"):
            name = h1.text

        photo = None
        if a_img := soup.select_one(".detail-img-zoom[href]"):
            photo = a_img.get("href")

        description = {}
        if rows := soup.select(".descr dl.row"):
            for row in rows:
                if key := row.select_one("dt"):
                    if value := row.select_one("dd"):
                        description[key.text.lower().strip()] = value.text.strip()

        if "цвет" not in description:
            description["цвет"] = "белый"

        price = None
        unit = None
        if price_span := soup.select_one(".price_in_int > span.span_price"):
            price, unit = self.parse_price(price_span.text)

        uid = None
        if uid_span := soup.select_one(".attrs p span.att_span"):
            uid = uid_span.text.strip()

        if not price or not unit or not uid:
            return

        return await parse(
            Page(
                uid=uid,
                url=url,
                price=price,
                unit=unit,
                photo=f"https://www.ekonomstroy.ru{photo}" if photo else "",
                description=description,
                name=name or "",
            ),
            soup,
        )

    @staticmethod
    def parse_price(price: str) -> tuple[int, str]:
        """
        Парсит цену с сайта и возвращает цену и единицу измерения (шт, м2, ...)
        """
        price_part, unit_part = price.split("/")
        return int("".join(filter(str.isdigit, price_part))), unit_part.lower().strip()

    @staticmethod
    def parse_as_float(value: str) -> float:
        return float(
            "".join(
                filter(lambda x: x in "0123456789" or x == ".", value.replace(",", "."))
            )
        )
