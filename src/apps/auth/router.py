from jose import jwt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, validator
from sqlalchemy.exc import IntegrityError

from ...settings import settings
from ...db.controllers.user_controller import get_user_by_username, create_new_user
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
    user = await get_user_by_username(credentials.username)
    # user = current_session.query(User)\
    #     .filter(User.username == credentials.username).first()
    if user and validate_password(credentials.password, user.password):
        token = jwt.encode(
            {'user_id': user.id},
            key=settings.JWT_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.post(path='/register')
async def register(credentials: AuthCredentials):
    try:
        new_user = await create_new_user(credentials.dict())
        if new_user:
            return {"user_id": new_user.id}
    except IntegrityError:
        raise HTTPException(status_code=400, detail='username: {} already exists'.format(credentials.username))
    raise HTTPException(status_code=400, detail='SMTH went wrong')
