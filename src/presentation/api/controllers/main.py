from fastapi import FastAPI

from .default import default_router
from .galery import router as galery_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(galery_router)
