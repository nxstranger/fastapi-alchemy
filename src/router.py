from fastapi import APIRouter
from src.users.router import router as user_router
from src.auth.router import router as auth_router

try:
    base_router = APIRouter(
        prefix='/api/v1'
    )

    base_router.include_router(user_router)
    base_router.include_router(auth_router)
except Exception as exc:
    print('exc:{}'.format(exc))

