from functools import lru_cache
from uuid import uuid4

from aiojobs import Scheduler
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)
from src.application.arts.commands.arts import (
    GetRandomArtCommand,
    GetRandomArtCommandHandler,
)
from src.application.arts.events.arts import GetRandomArtEventHandler
from src.domain.arts.events.arts import GetRandomArtEvent
from src.infrastructure.db.mongo import (
    ArtMongoDBService,
)
from src.infrastructure.db.services import (
    BaseArtMongoDBService,
)
from src.infrastructure.mediator.main import Mediator
from src.infrastructure.mediator.sub_mediators.event import EventMediator
from src.infrastructure.message_broker.base import BaseMessageBroker
from src.infrastructure.message_broker.kafka import KafkaMessageBroker
from src.settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def create_mongo_async_client():
        return AsyncIOMotorClient(
            config.mongo_db_connection_uri,
            serverSelectionTimeoutMS=3000,
        )

    container.register(
        AsyncIOMotorClient,
        factory=create_mongo_async_client,
        scope=Scope.singleton,
    )
    client = container.resolve(AsyncIOMotorClient)

    def init_mongodb_arts_service() -> BaseArtMongoDBService:
        return ArtMongoDBService(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_galery_database,
            mongo_db_collection=config.mongodb_arts_collection,
        )

    container.register(
        BaseArtMongoDBService,
        factory=init_mongodb_arts_service,
        scope=Scope.singleton,
    )

    # Handlers
    container.register(GetRandomArtCommandHandler)


    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        get_random_art_handler = GetRandomArtCommandHandler(
            _mediator=mediator,
            arts_service=container.resolve(BaseArtMongoDBService),
        )

        # event handlers
        random_art_handler_event = GetRandomArtEventHandler(
            broker_topic=config.recieved_random_art_topic,
            message_broker=container.resolve(BaseMessageBroker),
        )

        # events
        mediator.register_events(
            GetRandomArtEvent,
            [random_art_handler_event],
        )

        # commands
        mediator.register_command(
            GetRandomArtCommand,
            [get_random_art_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
