from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from .router import base_router, schema_redirect_router
from .settings import settings
from .api_schema import custom_openapi
from .apps.ws_app.ws_router import ws_route
from .middleware.cors_middleware import CustomCorsMiddleware
from .middleware.log_request_middleware import LogRequestMiddleware
from .middleware.auth_middleware import BearerWebsocketQuery


def get_app() -> FastAPI:
    application = FastAPI(
        description="Test project on FastAPI",
        version='0.0.7',
    )
    return application


app = get_app()

app.add_middleware(CustomCorsMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=BearerWebsocketQuery)

app.include_router(schema_redirect_router)

app.include_router(base_router)
app.include_router(ws_route)

app.openapi = custom_openapi(app)

if settings.COLLECT_CLICKHOUSE_DATA:
    app.add_middleware(LogRequestMiddleware)
