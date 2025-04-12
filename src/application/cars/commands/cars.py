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
    ) -> List:
        cars = await self.query_get_all_cars_service.get_all_cars(
            offset=command.offset,
        )
        schemas_cars = [CarSchema(**car) for car in cars]

        return schemas_cars
