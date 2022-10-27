from fastapi import Depends
from fastapi.routing import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError

from src.settings import settings
from src.middleware.auth_middleware import get_current_user
from src.db.user import User, RoleEnum
from src.db import current_session
from src.middleware.auth_middleware import UserJWT


router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {'description': 'Not found'}},
)


@router.get("/")
async def get_users(user: UserJWT = Depends(get_current_user)):
    if user.role_name != 'admin':
        users = current_session.query(User)\
            .where(User.id == user.id).order_by(User.id.asc()).all()
    else:
        users = current_session.query(User).all()
    return {'users': users}


class MakeMeAdminPayload(BaseModel):
    activation_code: str


@router.post('/make_me_admin')
async def make_me_admin(payload: MakeMeAdminPayload,
                        user: UserJWT = Depends(get_current_user)):

    if user.role_name == RoleEnum.ADMIN.value:
        raise HTTPException(status_code=400, detail='Already admin')

    if (
        settings.get('ADMIN_ACTIVATION_CODE') and
        payload.activation_code == settings.get('ADMIN_ACTIVATION_CODE') and
        user.role_name != RoleEnum.ADMIN.value
    ):
        user = current_session.query(User)\
            .where(User.id == user.id)\
            .update({User.role_name: RoleEnum.ADMIN.value}, synchronize_session='evaluate')
        current_session.commit()
        return {user}
    raise HTTPException(status_code=400, detail="Some error")

# @router.post("/", dependencies=[Depends(is_auth)])

