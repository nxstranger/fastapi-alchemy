from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from ..middleware.auth_middleware import UserJWT

from src.middleware.auth_middleware import get_current_user
from ..db import engine
# from ..users.models import User
from ..chat.models import Message

router = APIRouter(
    prefix='/messages',
    tags=['messages'],
    responses={404: {'description': 'Not found'}},
)


@router.get("/")
async def get_users(user: UserJWT = Depends(get_current_user)):
    if user:
        with Session(engine) as session:
            messages = session.query(Message).where(Message.sender_id == user.user_id).all()
        return {'messages': messages}
    return {'messages': []}
