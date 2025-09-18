from fastapi import FastAPI
from api.server.routes.users import router as UsersRouter
from api.server.routes.login import router as LoginRouter
from api.server.routes.info import router as InfoRouter
from api.server.utils.security import get_password_hash
from database.models import UserDbModel
from database.setup import global_init
from mongoengine import DoesNotExist
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:4000",
    "*",
]

global_init()

app = FastAPI()

# Create a default user
UserDbModel.objects(name="admin").update_one(
    role="admin", hashed_password=get_password_hash("1234"), upsert=True
)
   

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DoesNotExist)
async def unicorn_exception_handler(request, exc: DoesNotExist):
    return JSONResponse(
        status_code=404,
        content={"message": "Document not found"},
    )


app.include_router(InfoRouter, tags=["Info"], prefix="/info")
app.include_router(UsersRouter, tags=["Users"], prefix="/users")
app.include_router(LoginRouter, tags=["Login"], prefix="/login")
 
app.mount("/media", StaticFiles(directory="/media"), name="media")
