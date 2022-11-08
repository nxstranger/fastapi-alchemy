import datetime
from fastapi import WebSocket
from typing import Dict
import pprint


pp = pprint.PrettyPrinter(indent=2, depth=4)


class WebsocketConnection:

    def __init__(self, websocket: WebSocket):
        self.ws: WebSocket = websocket
        self._user = websocket.user
        self._contact = websocket.user.contact_id
        self._connected_at = datetime.datetime.now()

    def __repr__(self):
        try:
            return '<WebsocketConnection User: {}, Contact {}, Connected: {}>'.format(
                (self._user.id, self._user.username),
                self._user.contact_id,
                self._connected_at
            )
        except Exception as exc:
            print("CustomWebSocket error: {}".format(exc))
            return super().__repr__()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int: WebSocket] = {}

    async def connect(self, websocket: WebSocket):

        await websocket.accept()

        try:
            user_id = websocket.user.id
            if not user_id:
                return await websocket.close(4001)

            if not websocket.user.contact_id:
                return await websocket.close(code=4000, reason='Contact for user is not set')

            if self.get_connection(user_id):
                await self.disconnect_user(user_id)

            self.active_connections[user_id] = websocket
        except Exception as exc:
            print("ERROR ConnectionManager(connect): {}".format(exc))
            await self.disconnect(websocket)

    async def show_active_connections(self):
        try:
            [print(WebsocketConnection(x) for x in self.active_connections.values())]
        except Exception as exc:
            print("ERROR ConnectionManager(show_active_connections): {}".format(exc))

    async def delete_connection(self, user_id):
        try:
            self.active_connections.pop(user_id)
        except Exception as exc:
            print('ERROR ConnectionManager(delete_connection): {}'.format(exc))

    def get_connection(self, user_id: int):
        try:
            connection = self.active_connections.get(user_id)
            return connection if connection else None
        except Exception as exc:
            print("ERROR ConnectionManager(get_connection): {}".format(exc))

    async def disconnect(self, websocket: WebSocket):
        try:
            connection = self.get_connection(websocket.user.id)
            if connection:
                connection.close(1000)
            # todo: maybe add call alchemy - remove contact id
        except Exception as exc:
            print("ERROR ConnectionManager(disconnect): {}".format(exc))

    async def disconnect_user(self, user_id, disconnect_code=1000):
        try:
            user_connection: WebSocket = self.get_connection(user_id)
            if user_connection:
                await user_connection.close(disconnect_code)
                self.active_connections.pop(user_id)
            else:
                print('Its strange, connection not found')
        except Exception as exc:
            print('ERROR ConnectionManager(disconnect_user): {}'.format(exc))

    async def send_message_to_contact(self, data: object, ws_sender: WebSocket):
        contact_id = ws_sender.user.contact_id
        contact_websocket = self.get_connection(contact_id)
        if contact_websocket:
            await contact_websocket.send_json(data)
        else:
            await ws_sender.send_json({
                'type': 'ERR',
                'message': "Your contact isn't connected"
            })


manager = ConnectionManager()
