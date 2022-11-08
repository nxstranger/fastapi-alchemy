import json

from fastapi import WebSocket
from .manager import manager


async def handle_text_message(message_text: str, sender: WebSocket):
    try:
        # todo: encode for decode? add logic or simplify
        message_obj = json.loads(message_text)
        await manager.send_message_to_contact(message_obj, ws_sender=sender)
    except Exception as exc:
        # todo: handle exception
        print("ERROR handle_text_message: {}".format(exc))


def handle_data_message(data: bytes, sender: WebSocket):
    pass
