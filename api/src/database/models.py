from mongoengine import (
    Document,
    SequenceField,
    StringField
)



class UserDbModel(Document):
    idx = SequenceField()
    name = StringField()
    hashed_password = StringField()
    role = StringField(
        choices=["admin", "supervisor"], default=lambda: "admin")

    meta = {"db_alias": "interview_api", "collection": "users"}
