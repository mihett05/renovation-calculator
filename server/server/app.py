from contextlib import asynccontextmanager
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI
from di import create_container
from .api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")


setup_dishka(create_container(), app)
