from fastapi import Header, HTTPException
from jose import JWTError, jwt
from src.settings import settings


async def is_auth(authorization: str = Header()):
    if not authorization:
        return None
        # raise HTTPException(status_code=400, detail="Authorization is not provided")
    try:
        token = authorization.split(' ')[1]
        user = jwt.decode(token, key=settings.get('JWT_KEY'), algorithms=[settings.get('JWT_ALGORITHM')])
        if user:
            return user
        raise Exception('Invalid user')
    except Exception as exc:
        print('ERROR: {}'.format(exc))
        raise HTTPException(status_code=401, detail="Invalid token")
