from fastapi import Depends
from fastapi.routing import APIRouter, HTTPException

from ...settings import settings
from ...db import current_session
from ...db.user import User, RoleEnum
from ...db.controllers import user_controller
from ...middleware.auth_middleware import UserJWT, api_current_user
from .types import UpdateUserContactPayload, MakeMeAdminPayload

router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {'description': 'Not found'}},
)


@router.get("/")
async def get_users(user: UserJWT = Depends(api_current_user)):
    if user.role_name != 'admin':
        users = current_session.query(User)\
            .where(User.id == user.id).order_by(User.id.asc()).all()
    else:
        users = current_session.query(User).all()
    return {'users': users}


@router.post('/make_me_admin')
async def make_me_admin(payload: MakeMeAdminPayload,
                        user: UserJWT = Depends(api_current_user)):

    if user.role_name == RoleEnum.ADMIN.value:
        raise HTTPException(status_code=400, detail='Already admin')

    if (
        settings.ADMIN_ACTIVATION_CODE and
        payload.activation_code == settings.ADMIN_ACTIVATION_CODE and
        user.role_name != RoleEnum.ADMIN.value
    ):
        user = current_session.query(User)\
            .where(User.id == user.id)\
            .update({User.role_name: RoleEnum.ADMIN.value}, synchronize_session='evaluate')
        current_session.commit()
        return {user}
    raise HTTPException(status_code=400, detail="Some error")


@router.put('/update_contact')
async def update_user_contact(
        payload: UpdateUserContactPayload,
        user: UserJWT = Depends(api_current_user)
):
    try:
        contact = await user_controller.get_user_by_username(payload.contact_name)
        if contact:
            update_result = await user_controller.update_user_data(user.id, {'contact_id': contact.id})
            return update_result
    except Exception as exc:
        print('ERROR update_user_contact: {}'.format(exc))
    raise HTTPException(status_code=400)
