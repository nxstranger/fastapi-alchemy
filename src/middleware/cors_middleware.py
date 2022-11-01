from fastapi.middleware.cors import CORSMiddleware
from ..settings import settings

origins = settings.CORS_ORIGINS.split(',') if settings.CORS_ORIGINS else ('localhost', '127.0.0.1')

server_allow_methods = [
    # "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    # "PATCH",
    "POST",
    "PUT"
]


class CustomCorsMiddleware(CORSMiddleware):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=server_allow_methods,
            allow_headers=["*"],
        )

