from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database.models import UserDbModel
from api.server.dependencies.security import get_current_user
from api.server.schemas.login import TokenSchema
from api.server.schemas.users import UserShowSchema
from api.server.utils.security import (
    create_access_token,
    verify_password,
)


router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post("/access-token", response_model=TokenSchema)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user: UserDbModel = UserDbModel.objects.get(name=form_data.username)
    valid_hash = verify_password(form_data.password, user.hashed_password)
    if not valid_hash:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            str(user.id), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=UserShowSchema)
def test_token(current_user: UserDbModel = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
