from fastapi import FastAPI
from .router import base_router, schema_redirect_router
from .settings import settings
from .api_schema import custom_openapi
from .apps.wsapp.ws_router import ws_route
from .middleware.log_request_middleware import LogRequestMiddleware


def get_app() -> FastAPI:
    application = FastAPI(
        # **settings
    )
    return application


app = get_app()

# app.

app.include_router(base_router)
app.include_router(schema_redirect_router)
app.include_router(ws_route)

app.openapi = custom_openapi(app)

if settings.COLLECT_CLICKHOUSE_DATA:
    app.add_middleware(LogRequestMiddleware)


