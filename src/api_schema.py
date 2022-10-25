from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI


def custom_openapi(app: FastAPI):
    # if app.openapi_schema:
    #     return app.openapi_schema
    def get_schema():
        openapi_schema = get_openapi(
            title="Schema",
            version="0.0.1",
            description="This site is powered by FastAPI",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    return get_schema
