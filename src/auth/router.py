from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from ..users.models import User
from ..db import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from ..utils.crypto import validate_password
from src.settings import settings
from jose import jwt

router = APIRouter(
    prefix='/auth'
)


class AuthCredentials(BaseModel):
    username: str
    password: str

    @validator('username')
    def min_length_username(cls, val, **kwargs):      # noqa self->cls
        if len(val) < 3:
            raise ValueError('Should contain at least 3 symbols')
        return val

    # todo: more validation for username and password


@router.post(path='/login')
async def login(credentials: AuthCredentials):
    with Session(engine) as session:
        user = session.query(User)\
            .filter(User.username == credentials.username).first()
        print('user: {}'.format(user))
        if user and validate_password(credentials.password, user.password):
            print('P:{}\nH:{}'.format(credentials.password, user.password))
            token = jwt.encode({'user_id': user.id}, key=settings.get('JWT_KEY'), algorithm=settings.get('JWT_ALGORITHM'))
            return {'token': token}
        raise HTTPException(status_code=401, detail="Unauthorized")

    # return credentials.dict()


@router.post(path='/register')
async def register(credentials: AuthCredentials):
    new_user = User(**credentials.dict())
    # username = credentials.username
    with Session(engine) as session:
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            raise HTTPException(status_code=400, detail='username: {} already exists'.format(new_user.username))
        session.refresh(new_user)
        print(new_user)
        if new_user.id:
            return new_user
    raise HTTPException(status_code=400, detail='SMTH went wrong')
