from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

from src.application.cars.dto.car import DTOAllCars
from src.application.cars.schemas.base import CarSchema
from src.domain.common.commands.base import BaseCommands
from src.infrastructure.db.services import (
    BaseCommandCarsMongoDBService,
    BaseQueryCarsMongoDBService,
    BaseQueryParserCarsMongoDBService,
)
from src.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class ParserCarsCommand(BaseCommands):
    offset: int


@dataclass(frozen=True)
class ParserCarsCommandHandler(CommandHandler[ParserCarsCommand, DTOAllCars]):
    query_pasring_all_cars_service: BaseQueryParserCarsMongoDBService
    command_save_cars_service: BaseCommandCarsMongoDBService

    async def handle(
        self,
        command: ParserCarsCommand,
    ) -> Dict:
        cars = await self.query_pasring_all_cars_service.parser_cars_all_cars(
            offset=command.offset,
        )
        original_cars = cars.copy()

        await self.command_save_cars_service.save_cars_to_mongo(cars)

        return original_cars


@dataclass(frozen=True)
class GetAllCarsCommand(BaseCommands):
    offset: int


@dataclass(frozen=True)
class GetAllCarsCommandHandler(CommandHandler[GetAllCarsCommand, DTOAllCars]):
    query_get_all_cars_service: BaseQueryCarsMongoDBService

    async def handle(
        self,
        command: GetAllCarsCommand,
    ) -> List[CarSchema]:
        cars = await self.query_get_all_cars_service.get_all_cars(
            offset=command.offset,
        )
        schemas_cars = [CarSchema(**car) for car in cars]

        return schemas_cars


@dataclass(frozen=True)
class GetCarByIdCommand(BaseCommands):
    id_car: str


@dataclass(frozen=True)
class GetCarByIdCommandHandler(CommandHandler[GetCarByIdCommand, DTOAllCars]):
    query_get_car_by_id_service: BaseQueryCarsMongoDBService

    async def handle(
        self,
        command: GetCarByIdCommand,
    ) -> CarSchema:
        car = await self.query_get_car_by_id_service.get_car_by_id(
            id_car=command.id_car,
        )
        schemas_cars = CarSchema(**car)

        return schemas_cars


@dataclass(frozen=True)
class GetCarsByMarkCommand(BaseCommands):
    mark: str


@dataclass(frozen=True)
class GetCarsByMarkCommandHandler(CommandHandler[GetCarsByMarkCommand, DTOAllCars]):
    query_get_cars_by_mark_service: BaseQueryCarsMongoDBService

    async def handle(
        self,
        command: GetCarsByMarkCommand,
    ) -> CarSchema:
        cars = await self.query_get_cars_by_mark_service.get_cars_by_mark(
            mark=command.mark,
        )
        schemas_cars = [CarSchema(**car) for car in cars]

        return schemas_cars


@dataclass(frozen=True)
class GetCarsByYearCommand(BaseCommands):
    year: int


@dataclass(frozen=True)
class GetCarsByYearCommandHandler(CommandHandler[GetCarsByYearCommand, DTOAllCars]):
    query_get_cars_by_year_service: BaseQueryCarsMongoDBService

    async def handle(
        self,
        command: GetCarsByYearCommand,
    ) -> CarSchema:
        cars = await self.query_get_cars_by_year_service.get_cars_by_year(
            year=command.year,
        )
        schemas_cars = [CarSchema(**car) for car in cars]

        return schemas_cars
