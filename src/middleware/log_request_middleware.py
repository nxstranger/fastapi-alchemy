from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel


class StatData(BaseModel):
    client: str
    path: str
    method: str
    agent: str
    stamp: datetime


async def insert_stat(data: StatData):
    from ..clickhouse import client, REQUESTS_STATS_TABLE

    client.execute(
        "INSERT INTO {} (client, path, method, agent, stamp) VALUES".format(REQUESTS_STATS_TABLE),
        [data.dict()]
    )


class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        stat_data = StatData(**{
            "client": str(request.scope.get('client')),
            "method": request.method,
            "agent": request.headers.get('user-agent'),
            "path": request.scope.get('path'),
            "stamp": datetime.now(),
        })
        await insert_stat(data=stat_data)
        response = await call_next(request)
        return response
