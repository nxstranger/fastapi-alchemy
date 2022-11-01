from pydantic import BaseModel


class MakeMeAdminPayload(BaseModel):
    activation_code: str


class UpdateUserContactPayload(BaseModel):
    contact_name: str


