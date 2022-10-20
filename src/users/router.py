from fastapi import Depends
from fastapi.routing import APIRouter
from src.auth.auth_middleware import is_auth

router = APIRouter(
    prefix="/items",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(is_auth)])
async def get_users():
    return {'users': []}


# @router.post("/", dependencies=[Depends(is_auth)])

