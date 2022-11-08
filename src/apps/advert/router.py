import json
from bson import json_util, ObjectId
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
    tags=['advert']
)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@router.post('/')
async def create_adv(payload: NewAdvPayload):
    try:
        insert_id = await insert_advert({**payload.new_adv, 'created_at': datetime.now().timestamp()})
        return {"response": str(insert_id)}
    except Exception as exc:
        print("ERROR create_adv: {}", format(exc))
    raise HTTPException(status_code=400)


@router.get('/')
async def adverts(page: int = 0, limit: int = 10):

    try:
        result = await get_adverts(limit=limit, page=page)
        # return json.loads(json_util.dumps(result))
        return {"result": JSONEncoder().encode(result)}
        # return {'data': json_util.loads(result)}
    except Exception as exc:
        # return {"result": []}
        print("ERROR show_adverts: {}".format(exc))
    raise HTTPException(status_code=400)


@router.get('/{id}')
async def advert_by_id(adv_id: str):
    try:
        result = await get_advert_by_id(adv_id)
        return json.loads(json_util.dumps(result))
    except Exception as exc:
        print("ERROR get_advert: {}".format(exc))
    raise HTTPException(status_code=400)
