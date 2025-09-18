from fastapi import Depends, HTTPException, status , Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from api.server.schemas.login import TokenPayloadSchema
from database.models import UserDbModel
from pydantic import ValidationError

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "ASDASD"
API_KEY = "pHLiRC+i4c8iwGFgFjpHF10ro52gr3FUWB/tH6CvhFg"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDbModel:
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayloadSchema(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = UserDbModel.objects.get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True 