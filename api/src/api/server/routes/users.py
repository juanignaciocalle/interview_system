from typing import List
from fastapi import APIRouter, Depends, Request
from api.server.dependencies.security import get_current_user

from api.server.schemas.users import UserCreateSchema, UserShowSchema, UserCreateSchema

from api.server.utils.mongo import apply_query_params
from api.server.utils.security import get_password_hash

from database.models import UserDbModel

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_description="User created", response_model=UserShowSchema)
def create_pcs_user(user: UserCreateSchema):
    mongo_user = UserDbModel(
        name=user.name, role=user.role, hashed_password=get_password_hash(
            user.password)
    )
    mongo_user.save()
    return mongo_user.to_mongo()


@router.put(
    "/{id}/", response_description="User updated", response_model=UserShowSchema
)
def update_pcs_alert_user(id: str, user: UserCreateSchema):
    mongo_user: UserDbModel = UserDbModel.objects.get(id=id)
    update_dict = user.dict(exclude_unset=True)
    for k in update_dict.keys():
        setattr(mongo_user, k, update_dict[k])
    mongo_user.save()
    mongo_user: UserDbModel = UserDbModel.objects.get(id=id)
    return mongo_user.to_mongo()


@router.get(
    "/", response_description="Process retrieved", response_model=List[UserShowSchema]
)
def get_pcs_alert_users(request: Request):
    qp = request.query_params
    queryset = apply_query_params(UserDbModel.objects, qp)
    print(list(queryset.as_pymongo()))
    return list(queryset.as_pymongo())


@router.get(
    "/{id}/",
    response_description="Process data retrieved",
    response_model=UserShowSchema,
)
def get_pcs_process_data(id):
    mongo_user: UserDbModel = UserDbModel.objects.get(id=id)
    return mongo_user.to_mongo()


@router.delete("/{id}/", response_description="Process data deleted from the database")
def delete_pcs_process_data(id: str):
    mongo_user: UserDbModel = UserDbModel.objects.get(id=id)
    mongo_user.delete()
    return None
