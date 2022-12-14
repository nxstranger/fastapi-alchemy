from fastapi.middleware.cors import CORSMiddleware
from ..settings import settings

DEFAULT_ORIGINS = ('http://localhost:8000', 'http://127.0.0.1/8000')

try:
    origins = settings.CORS_ORIGINS.split(',') if settings.CORS_ORIGINS else DEFAULT_ORIGINS
except Exception as exc:
    print('PARSE ORIGINS ERROR: {}'.format(exc))
    origins = DEFAULT_ORIGINS

print('\nCORS origins: {}\n'.format(origins))

# origins = [
#     'http://localhost:8000',
#     'http://localhost:3000',
#     # 'http://localhost:8000',
#     # 'http://127.0.0.1:8000',
#     # 'http://192.168.1.71:3000',
#     # 'http://192.168.1.71:8000',
# ]

origins_regex = r'^http://192.168.[0-1].[0-9]{1,3}:[3,8]000$'

# print("SERVER ORIGINS: {}".format(origins))

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
            allow_origin_regex=origins_regex,
            allow_credentials=True,
            allow_methods=server_allow_methods,
            allow_headers=["*"],
        )
