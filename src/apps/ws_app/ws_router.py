import json
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.routing import APIRouter
from .manager import manager

ws_route = APIRouter(
    prefix='/private',
    tags=['ws'],
)


@ws_route.websocket('/')
async def handle(websocket: WebSocket, background_tasks: BackgroundTasks):
    print('websocket: {}'.format(websocket))
    print('websocket: {}'.format(websocket.scope))
    await manager.connect(websocket)

    connection_time = datetime.now()
    try:
        while True:
            print(websocket.user)
            some_data_receive = await websocket.receive()

            print('some_data_receive: {}'.format(some_data_receive))
            print('timestamp: {}'.format(datetime.now().timestamp()))
            print('timestamp int: {}'.format(
                    int(datetime.now().timestamp())
            ))
            answer = {
                'type': 'MSG',
                'stamp': int(datetime.now().timestamp() * 1000),
                'message': "It's amazing",
            }
            await websocket.send_json(data=answer)

            if (datetime.now() - connection_time).total_seconds() > 100:
                print('close by timeout')
                return
    except WebSocketDisconnect:
        manager.disconnect(websocket)
