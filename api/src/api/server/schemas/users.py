from pydantic import Field

from api.server.utils.mongo import OID, MongoModel

BASE_USER_EXAMPLE = {
    "name": "admin",
    "role": "admin",
}


class UserBaseSchema(MongoModel):
    name: str = Field(...)
    role: str = Field(...)

    class Config:
        json_schema_extra = {"example": BASE_USER_EXAMPLE}


class UserCreateSchema(UserBaseSchema):
    password: str = Field(...)

    class Config:
        _EXAMPLE = BASE_USER_EXAMPLE.copy()
        _EXAMPLE["password"] = "1234"
        json_schema_extra = {"example": _EXAMPLE}
        from_attributes = True


class UserShowSchema(UserBaseSchema):
    id: OID = Field(alias="_id")

    class Config:
        _EXAMPLE = BASE_USER_EXAMPLE.copy()
        _EXAMPLE["_id"] = "62c8c2cde8b0d286875e05d8"
        json_schema_extra = {"example": _EXAMPLE}
        from_attributes = True


class UserCredentialsSchema(MongoModel):
    name: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "admin",
                "password": "1234",
            }
        }
