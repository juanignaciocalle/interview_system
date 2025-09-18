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
    if not user:
        disconnect(alias="interview_api")
        return {"statusCode": 404, "body": "User not found"}

    user.delete()
    disconnect(alias="interview_api")
    return {"statusCode": 200, "body": f"User {username} deleted"}