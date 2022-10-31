from fastapi import HTTPException, status, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import load_only
from ..settings import settings
from ..db import User, current_session
from ..db.user import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login')


class UserJWT(BaseModel):
    id: int
    is_active: bool
    role_name: RoleEnum

    class Config:
        use_enum_values = True


async def jwt_user(token: str = Depends(oauth2_scheme)):
    try:
        user = jwt.decode(token, key=settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = user.get('user_id')
        if user:
            # TODO: move to controllers
            db_user = current_session.query(User)\
                .options(load_only(User.id, User.is_active, User.role_name))\
                .filter(User.id == user_id).first()
            return db_user
    except Exception as exc:
        print('ERROR: {}'.format(exc))
        raise HTTPException(status_code=401, detail='Invalid token')


async def is_auth(user: UserJWT = Depends(jwt_user)):
    if user:
        return True
    return False


async def get_current_user(user: UserJWT = Depends(jwt_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def is_user_admin(user: UserJWT = Depends(get_current_user)):
    if user == 'admin':
        return True
    return False

