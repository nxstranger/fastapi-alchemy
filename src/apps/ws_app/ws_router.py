import json
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.routing import APIRouter
from starlette.websockets import WebSocketState
from .manager import manager
from .handler import handle_data_message, handle_text_message

ws_route = APIRouter(
    prefix='/private',
    tags=['ws'],
)


@ws_route.websocket('/')
async def private_chat(websocket: WebSocket, background_tasks: BackgroundTasks):
    await manager.connect(websocket)

    try:
        while True:
            message = await websocket.receive()

            if websocket.client_state == WebSocketState.DISCONNECTED:
                await manager.delete_connection(websocket.user.id)
                return

            available_modes = {'text', 'binary'}
            mode = (message.keys() & available_modes).pop()
            if mode == 'text':
                await handle_text_message(message['text'], websocket)
            elif mode == 'binary':
                handle_data_message(message['binary'], websocket)

    except WebSocketDisconnect:
        print('WebSocketDisconnect Exception')
        await websocket.close()
    except Exception as exc:
        print("ERROR WS handle_message: {}".format(exc))
        await manager.disconnect(websocket)

