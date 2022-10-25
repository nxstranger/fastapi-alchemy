from fastapi import APIRouter
from src.user.router import router as user_router
from src.auth.router import router as auth_router
from src.chat.router import router as chat_router

try:
    base_router = APIRouter(
        prefix='/api/v1'
    )

    base_router.include_router(user_router)
    base_router.include_router(auth_router)
    base_router.include_router(chat_router)
except Exception as exc:
    print('Error:{}'.format(exc))

