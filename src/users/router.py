from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session
from src.middleware.auth_middleware import get_current_user
from .models import User
from ..db import engine
from ..middleware.auth_middleware import UserJWT

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}},
)


@router.get("/")
async def get_users(user: UserJWT = Depends(get_current_user)):
    with Session(engine) as session:
        print('user: {}'.format(user))
        if user.role_name != 'admin':
            users = session.query(User)\
                .where(User.id == user.user_id).order_by(User.id.asc()).all()
        else:
            users = session.query(User).all()
        print('len: {}\nusers: {}'.format(len(users), users))
        return {'users': users}

# @router.post("/", dependencies=[Depends(is_auth)])

