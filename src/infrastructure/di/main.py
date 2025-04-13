from functools import lru_cache

from aiojobs import Scheduler
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)
from src.application.cars.commands.cars import (
    CreatingCarCommand,
    CreatingCarCommandHandler,
    DeletingCarByIDCommand,
    DeletingCarByIDCommandHandler,
    FilterCarsCommand,
    FilterCarsCommandHandler,
    GetAllCarsCommand,
    GetAllCarsCommandHandler,
    GetCarByIdCommand,
    GetCarByIdCommandHandler,
    GetCarsByMarkCommand,
    GetCarsByMarkCommandHandler,
    GetCarsByYearCommand,
    GetCarsByYearCommandHandler,
    ParserCarsCommand,
    ParserCarsCommandHandler,
    PuttingCarCommand,
    PuttingCarCommandHandler,
)
from src.infrastructure.db.mongo import (
    CommandCarsMongoDBService,
    CommandCarsParserMongoDBService,
    QueryCarsMongoDBService,
    QueryParserCarsMongoDBService,
)
from src.infrastructure.db.services import (
    BaseCommandCarsMongoDBService,
    BaseCommandCarsParserMongoDBService,
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

    def init_mongodb_cars_from_parser_service() -> BaseCommandCarsParserMongoDBService:
        return CommandCarsParserMongoDBService(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_galery_database,
            mongo_db_collection=config.mongodb_cars_collection,
        )

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
        BaseCommandCarsParserMongoDBService,
        factory=init_mongodb_cars_from_parser_service,
        scope=Scope.singleton,
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
    container.register(GetCarByIdCommandHandler)
    container.register(GetCarsByMarkCommandHandler)
    container.register(GetCarsByYearCommandHandler)
    container.register(DeletingCarByIDCommandHandler)
    container.register(CreatingCarCommandHandler)
    container.register(PuttingCarCommandHandler)
    container.register(FilterCarsCommandHandler)

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
            command_save_cars_service=container.resolve(
                BaseCommandCarsParserMongoDBService,
            ),
        )

        # command handlers
        getting_car_by_id_handler = GetCarByIdCommandHandler(
            _mediator=mediator,
            query_get_car_by_id_service=container.resolve(BaseQueryCarsMongoDBService),
        )

        # command handlers
        getting_cars_by_mark_handler = GetCarsByMarkCommandHandler(
            _mediator=mediator,
            query_get_cars_by_mark_service=container.resolve(
                BaseQueryCarsMongoDBService,
            ),
        )
        # command handlers
        getting_cars_by_year_handler = GetCarsByYearCommandHandler(
            _mediator=mediator,
            query_get_cars_by_year_service=container.resolve(
                BaseQueryCarsMongoDBService,
            ),
        )

        # command handlers
        deleting_car_by_id_handler = DeletingCarByIDCommandHandler(
            _mediator=mediator,
            command_deleting_car_service=container.resolve(
                BaseCommandCarsMongoDBService,
            ),
        )

        # command handlers
        creating_car_handler = CreatingCarCommandHandler(
            _mediator=mediator,
            command_creating_car_service=container.resolve(
                BaseCommandCarsMongoDBService,
            ),
        )

        # command handlers
        putting_car_handler = PuttingCarCommandHandler(
            _mediator=mediator,
            command_putting_car_service=container.resolve(
                BaseCommandCarsMongoDBService,
            ),
            query_putting_car_service=container.resolve(
                BaseQueryCarsMongoDBService,
            ),
        )

        # command handlers
        filter_cars_handler = FilterCarsCommandHandler(
            _mediator=mediator,
            query_filter_cars_service=container.resolve(
                BaseQueryCarsMongoDBService,
            ),
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

        # commands
        mediator.register_command(
            GetCarByIdCommand,
            [getting_car_by_id_handler],
        )

        # commands
        mediator.register_command(
            GetCarsByMarkCommand,
            [getting_cars_by_mark_handler],
        )

        # commands
        mediator.register_command(
            GetCarsByYearCommand,
            [getting_cars_by_year_handler],
        )

        # commands
        mediator.register_command(
            DeletingCarByIDCommand,
            [deleting_car_by_id_handler],
        )

        # commands
        mediator.register_command(
            CreatingCarCommand,
            [creating_car_handler],
        )

        # commands
        mediator.register_command(
            PuttingCarCommand,
            [putting_car_handler],
        )

        # commands
        mediator.register_command(
            FilterCarsCommand,
            [filter_cars_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
