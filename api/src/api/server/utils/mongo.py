from datetime import datetime
from typing import List
from typing_extensions import Annotated
from bson import ObjectId
from pydantic import BaseConfig, BaseModel, PlainSerializer
import mongoengine
from typing import Any
from bson import ObjectId
from pydantic_core import core_schema


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        # It can also be a mongoengine object
        try:
            return v.id
        except:
            pass
        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, _handler
    ) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _, handler):
        return handler(core_schema.str_schema())


OID = Annotated[ObjectId, ObjectIdPydanticAnnotation]


class MongoModel(BaseModel):
    class Config(BaseConfig):
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }


def datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except:
        return False
    return True


def apply_query_params(
    query_set: mongoengine.QuerySet, query_params: dict, exclude: List[str] = []
):
    limit = None
    skip = None
    order_by = None

    params_dict = {}

    for key in query_params:
        params_dict[key] = query_params[key]
        if params_dict[key] in ["false", "true"]:
            params_dict[key] = True if params_dict[key] == "true" else False
        if datetime_valid(params_dict[key]):
            params_dict[key] = datetime.fromisoformat(
                params_dict[key].replace("Z", "+00:00")
            )

    if "limit" in params_dict:
        limit = int(params_dict["limit"])
        params_dict.pop("limit")

    if "skip" in params_dict:
        skip = int(params_dict["skip"])
        params_dict.pop("skip")

    if "order_by" in params_dict:
        order_by = params_dict["order_by"]
        params_dict.pop("order_by")

    for key in exclude:
        if key in params_dict:
            params_dict.pop(key)

    query_set = query_set.filter(**params_dict)
    if order_by is not None:
        query_set = query_set.order_by(order_by)
    if limit is not None:
        query_set = query_set.limit(limit)
    if skip is not None:
        query_set = query_set.skip(skip)

    return query_set
