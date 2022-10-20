from fastapi import FastAPI
from src.router import base_router
from src.settings import settings
# from src.db import Base
# from .db import engine


def get_app() -> FastAPI:
    application = FastAPI(**settings)
    # Base.metadata.bind = engine
    return application


app = get_app()

app.include_router(base_router)

