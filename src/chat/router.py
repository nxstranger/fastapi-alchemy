from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from ..middleware.auth_middleware import UserJWT

from src.middleware.auth_middleware import get_current_user
from ..db import current_session
from src.db.chat import Message

router = APIRouter(
    prefix='/messages',
    tags=['messages'],
    responses={404: {'description': 'Not found'}},
)


@router.get("/")
async def get_users(user: UserJWT = Depends(get_current_user)):
    if user:
        messages = current_session.query(Message).where(Message.sender_id == user.id).all()
        return {'messages': messages}
    return {'messages': []}
