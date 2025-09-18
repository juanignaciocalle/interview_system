import os
from mongoengine import connect, disconnect
from api.src.database.models import UserDbModel

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/interview_db")

def lambda_handler(event, context):
    username = event.get("username")
    password = event.get("password")
    if not username or not password:
        return {"statusCode": 400, "body": "Missing username or password"}

    connect(host=MONGO_URL, alias="interview_api")
    if UserDbModel.objects(name=username).first():
        disconnect(alias="interview_api")
        return {"statusCode": 409, "body": "User already exists"}

    user = UserDbModel(name=username, hashed_password=password)
    user.save()
    disconnect(alias="interview_api")
    return {"statusCode": 201, "body": f"User {username} added"}