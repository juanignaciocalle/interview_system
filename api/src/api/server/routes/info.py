from fastapi import APIRouter
from config.common import API_VERSION

router = APIRouter()


@router.get("/apiversion")
def get_api_version():
    return {"version": API_VERSION}
