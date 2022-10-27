from fastapi import WebSocket


async def handle(websocket: WebSocket):
    print('websocket: {}'.format(websocket))
    await websocket.accept()
    await websocket.close()
    pass
