import json
from bson import json_util
from datetime import datetime
from fastapi.routing import APIRouter, HTTPException
from .types import NewAdvPayload

from .advert_controller import (
    insert_advert,
    get_adverts,
    get_advert_by_id
)

router = APIRouter(
    prefix='/advert',
    tags=['adverts']
)


# @router.get(path='/show_databases')
# async def databases():
#     try:
#         rez = await show_databases()
#         print(rez)
#         return rez
#     except Exception as exc:
#         print("ERROR: {}".format(exc))
#         HTTPException(status_code=400)


# @router.post('/create_new_table')
# async def create_table(payload: TableNamePayload):
#     try:
#         rez = await create_new_table(payload.table_name)
#         print(rez)
#         return rez
#     except Exception as exc:
#         print("ERROR: {}".format(exc))
#         HTTPException(status_code=400)


@router.post('/advert')
async def create_adv(payload: NewAdvPayload):
    try:
        insert_id = await insert_advert({**payload.new_adv, 'created_at': datetime.now().timestamp()})
        return {"response": str(insert_id)}
    except Exception as exc:
        print("ERROR: {}", format(exc))
    return HTTPException(status_code=400)


@router.get('/advert')
async def show_adverts(page: int = 0, limit: int = 10):
    try:
        result = await get_adverts(limit=limit, page=page)
        print(result)
        return json.loads(json_util.dumps(result))

    except Exception as exc:
        print("ERROR: {}".format(exc))
    return HTTPException(status_code=400)


@router.get('/advert/{id}')
async def get_advert(adv_id: str):
    try:
        result = await get_advert_by_id(adv_id)
        return json.loads(json_util.dumps(result))
    except Exception as exc:
        print("ERROR: {}".format(exc))
    return HTTPException(status_code=400)
