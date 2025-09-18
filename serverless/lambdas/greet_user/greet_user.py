import os
from mongoengine import connect, disconnect
from api.src.database.models import UserDbModel

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/interview_db")

def lambda_handler(event, context):
    username = event.get("username")
    if not username:
        return {"statusCode": 400, "body": "Missing username"}

    connect(host=MONGO_URL, alias="interview_api")
    user = UserDbModel.objects(name=username).first()
    disconnect(alias="interview_api")

    if user:
        return {"statusCode": 200, "body": f"Hello from Lambda, {username}!"}
    else:
        return {"statusCode": 200, "body": "Hi, Who are you?"}