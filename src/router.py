from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from .apps.user.router import router as user_router
from .apps.auth.router import router as auth_router
from .apps.chat.router import router as chat_router
from .apps.advert.router import router as advert_router


schema_redirect_router = APIRouter(
    prefix='',
)


@schema_redirect_router.get('/')
async def redirect_to_schema():
    return RedirectResponse(url='/docs')


try:
    base_router = APIRouter(
        prefix='/api/v1'
    )

    base_router.include_router(user_router)
    base_router.include_router(auth_router)
    base_router.include_router(chat_router)
    base_router.include_router(advert_router)
except Exception as exc:
    print('Error:{}'.format(exc))

