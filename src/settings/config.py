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
    mongodb_arts_collection: str = Field(
        default="arts",
        alias="MONGODB_ARTS_COLLECTION",
    )
    mongodb_flowers_collection: str = Field(
        default="flowers",
        alias="MONGODB_FLOWERS_COLLECTION",
    )
    mongodb_poems_collection: str = Field(
        default="poems",
        alias="MONGODB_POEMS_COLLECTION",
    )
    kafka_url: str = Field(
        default="kafka:29092",
        alias="KAFKA_URL",
    )
    recieved_random_art_topic: str = Field(default="recieved_random_art")
    recieved_random_flower_topic: str = Field(default="recieved_random_flower")
    recieved_random_poem_topic: str = Field(default="recieved_random_poem")

    debug: bool = Field(default=True, alias="DEBUG")
