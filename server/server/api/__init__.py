from fastapi import APIRouter

from .catalog import catalog_router

router = APIRouter()

router.include_router(catalog_router, prefix="/catalog")
