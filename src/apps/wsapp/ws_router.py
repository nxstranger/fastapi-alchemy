from fastapi.routing import APIRouter, WebSocket
from .handler import handle


ws_route = APIRouter(
    prefix='/private',
    tags=['ws']
)


@ws_route.websocket('/')
async def handle(websocket: WebSocket):
    print('websocket: {}'.format(websocket))
    await websocket.accept()
    # await websocket.close()
    pass
