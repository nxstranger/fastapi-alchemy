from jose import jwt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, validator
from sqlalchemy.exc import IntegrityError

from ...settings import settings
from ...db.user import User
from ...db import current_session
from ...utils.crypto import validate_password

router = APIRouter(
    prefix='/auth',
    tags=["auth"],
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
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = current_session.query(User)\
        .filter(User.username == credentials.username).first()
    if user and validate_password(credentials.password, user.password):
        token = jwt.encode(
            {'user_id': user.id},
            key=settings.get('JWT_KEY'),
            algorithm=settings.get('JWT_ALGORITHM')
        )
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.post(path='/register')
async def register(credentials: AuthCredentials):
    new_user = User(**credentials.dict())
    # with Session(engine) as session:
    current_session.add(new_user)
    try:
        current_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail='username: {} already exists'.format(new_user.username))
    current_session.refresh(new_user)
    if new_user.id:
        return {"user_id": new_user.id}
    raise HTTPException(status_code=400, detail='SMTH went wrong')
