from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongo_db_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongo_db_admin_password: str = Field(alias="MONGO_DB_ADMIN_PASSWORD")
    mongo_db_admin_username: str = Field(
        default="admin",
        alias="MONGO_DB_ADMIN_USERNAME",
    )
    mongodb_galery_database: str = Field(
        default="galery",
        alias="MONGODB_GALERY_DATABASE",
    )
    mongodb_cars_collection: str = Field(
        default="cars",
        alias="MONGODB_CARS_COLLECTION",
    )

    debug: bool = Field(default=True, alias="DEBUG")
