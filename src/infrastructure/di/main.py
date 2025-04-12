from functools import lru_cache

from aiojobs import Scheduler
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)
from src.application.cars.commands.cars import (
    GetAllCarsCommand,
    GetAllCarsCommandHandler,
    ParserCarsCommand,
    ParserCarsCommandHandler,
)
from src.infrastructure.db.mongo import (
    CommandCarsMongoDBService,
    QueryCarsMongoDBService,
    QueryParserCarsMongoDBService,
)
from src.infrastructure.db.services import (
    BaseCommandCarsMongoDBService,
    BaseQueryCarsMongoDBService,
)
from src.infrastructure.mediator.main import Mediator
from src.infrastructure.mediator.sub_mediators.event import EventMediator
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

    def init_mongodb_cars_service() -> BaseCommandCarsMongoDBService:
        return CommandCarsMongoDBService(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_galery_database,
            mongo_db_collection=config.mongodb_cars_collection,
        )

    def init_mongodb_getting_cars_service() -> BaseQueryCarsMongoDBService:
        return QueryCarsMongoDBService(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_galery_database,
            mongo_db_collection=config.mongodb_cars_collection,
        )

    container.register(
        BaseCommandCarsMongoDBService,
        factory=init_mongodb_cars_service,
        scope=Scope.singleton,
    )

    container.register(
        BaseQueryCarsMongoDBService,
        factory=init_mongodb_getting_cars_service,
        scope=Scope.singleton,
    )

    # Handlers
    container.register(GetAllCarsCommandHandler)
    container.register(ParserCarsCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        get_all_cars_handler = GetAllCarsCommandHandler(
            _mediator=mediator,
            query_get_all_cars_service=container.resolve(BaseQueryCarsMongoDBService),
        )

        # command handlers
        parsing_all_cars_handler = ParserCarsCommandHandler(
            _mediator=mediator,
            query_pasring_all_cars_service=QueryParserCarsMongoDBService(),
            command_save_cars_service=container.resolve(BaseCommandCarsMongoDBService),
        )

        # commands
        mediator.register_command(
            GetAllCarsCommand,
            [get_all_cars_handler],
        )

        # commands
        mediator.register_command(
            ParserCarsCommand,
            [parsing_all_cars_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
