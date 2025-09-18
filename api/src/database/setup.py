import mongoengine
from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    database_name: str = "interview_api"
    database_user: str = ""
    database_password: str = ""
    database_port: int = 27017
    database_host: str = "localhost"


def init_database(db_name, host=None, port=None, username=None, password=None):
    mongoengine.register_connection(
        alias=db_name,
        name=db_name,
        username=username,
        password=password,
        authentication_source="admin",
        port=port,
        host=host,
    )
    mongoengine.connect(
        db_name,
        username=username,
        password=password,
        authentication_source="admin",
        host=host,
        port=port,
    )


def global_init():
    db_settings = DbSettings()

    init_database(
        db_name=db_settings.database_name,
        host=db_settings.database_host,
        port=db_settings.database_port,
        username=db_settings.database_user,
        password=db_settings.database_password,
    )
