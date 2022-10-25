from fastapi import Header, HTTPException, status, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login')


class UserJWT(BaseModel):
    user_id: int
    role_name: str


async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        # print('token: {}'.format(token))
        user = jwt.decode(token, key=settings.get('JWT_KEY'), algorithms=[settings.get('JWT_ALGORITHM')])
        jwt_user = UserJWT(**user)
        return jwt_user
    except Exception as exc:
        print('ERROR: {}'.format(exc))
        raise HTTPException(status_code=401, detail='Invalid token')


async def is_auth(user: UserJWT = Depends(get_token)):
    if user:
        return True
    return False


async def get_current_user(user: UserJWT = Depends(get_token)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def is_user_admin(user: UserJWT = Depends(get_current_user)):
    if user.role_name == 'admin':
        return True
    return False

