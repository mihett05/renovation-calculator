import argparse
import asyncio

from settings import get_settings
from storage.postgres import PostgresSaver
from storage.postgres.models.base import get_engine, get_session_maker
from uvicorn import run
from worker.sites.ekonomstroy.parser import EkonomstroyParser


async def main():
    settings = get_settings()
    engine = get_engine(str(settings.postgres_url))
    session_maker = get_session_maker(engine)
    async with session_maker() as session:
        saver = PostgresSaver(session)
        async with EkonomstroyParser(saver) as parser:
            await parser.parse_catalog()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog="Renovation calculator")
    arg_parser.add_argument("--worker", default=False, action="store_true")
    args = arg_parser.parse_args()
    if args.worker:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    else:
        run(
            "server.app:app",
            host="0.0.0.0",
            port=8000,
            reload=get_settings().debug,
        )
