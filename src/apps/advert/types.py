import json
from pydantic import BaseModel, Json
#
#
# class TableNamePayload(BaseModel):
#     table_name: str
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "table_name": "advert"
#             }
#         }


class NewAdvPayload(BaseModel):
    new_adv: Json

    class Config:
        schema_extra = {
            "example": {
                "new_adv": json.dumps({
                    'name': "motorbike",
                    'price': 500,
                }),
            }
        }