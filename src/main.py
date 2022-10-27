from fastapi import FastAPI
from src.router import base_router
from src.settings import settings
from .api_schema import custom_openapi
from .apps.wsapp.ws_router import ws_route


def get_app() -> FastAPI:
    application = FastAPI(**settings)
    return application


app = get_app()

app.include_router(base_router)
app.include_router(ws_route)

app.openapi = custom_openapi(app)


