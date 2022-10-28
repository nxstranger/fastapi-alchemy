from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from src.middleware.auth_middleware import UserJWT, is_auth
from pydantic import BaseModel

from src.middleware.auth_middleware import get_current_user
from src.db.controllers.message_controller import get_user_messages, create_message

router = APIRouter(
    prefix='/message',
    tags=['messages'],
    responses={404: {'description': 'Not found'}},
)


@router.get("/")
async def get_my_messages(user: UserJWT = Depends(get_current_user)):
    if user:
        messages = get_user_messages(user.id)
        return {'messages': messages}
    return {'messages': []}


class MessagePayload(BaseModel):
    receiver_id: int
    text: str


@router.post('/', dependencies=[Depends(is_auth)])
async def post_message(payload: MessagePayload, user: UserJWT = Depends(get_current_user)):
    try:
        new_id = await create_message(**payload.dict(), user_id=user.id)
        return {'messageId': new_id}
    except Exception as exc:
        print('ERROR: {}'.format(exc))
        HTTPException(status_code=400)
