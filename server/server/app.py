from contextlib import asynccontextmanager
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from di import create_container
from .api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://renovator.lovepaw.ru",
        "https://lovepaw.ru",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

setup_dishka(create_container(), app)
