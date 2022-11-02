from fastapi import HTTPException, status, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import HTTPConnection
from jose import jwt
from starlette.middleware.authentication import AuthenticationBackend
from ..settings import settings
from ..db.controllers import user_controller
from ..db.user import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login')


class UserJWT(BaseModel):
    id: int
    is_active: bool
    role_name: RoleEnum

    class Config:
        use_enum_values = True


async def decode_token(token: str):
    try:
        user = jwt.decode(token, key=settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
        return user.get('user_id')
    except Exception as exc:
        print('ERROR decode_token: {}'.format(exc))
    return None


async def user_from_headers(token: str = Depends(oauth2_scheme)):
    try:
        user_id = await decode_token(token)
        db_user = await user_controller.get_active_user_by_id(user_id)
        return db_user
    except Exception as exc:
        print('ERROR user_from_headers: {}'.format(exc))
        raise HTTPException(status_code=401, detail='Invalid token')


async def is_auth(user: UserJWT = Depends(user_from_headers)):
    if user:
        return True
    return False


async def api_current_user(user: UserJWT = Depends(user_from_headers)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def is_user_admin(user: UserJWT = Depends(api_current_user)):
    if user == 'admin':
        return True
    return False


class BearerWebsocketQuery(AuthenticationBackend):

    async def authenticate(self: HTTPConnection, *args, **kwargs):
        try:
            connection_type = self.scope.get('type')
            query_token = self.query_params.get('token')
            if connection_type == 'websocket':
                tkn = query_token.split(' ')[1]
                user_id = await decode_token(token=tkn)
                db_user = await user_controller.get_active_user_by_id(user_id)
                return query_token, db_user
        except Exception as exc:
            print("ERROR BearerWebsocketQuery: {}".format(exc))
        return None, None
