from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

from fastapi import HTTPException
from src.application.cars.dto.car import DTOCars
from src.application.cars.schemas.base import (
    CarSchema,
    CarUpdateSchema,
)
from src.domain.cars.exceptions.car import IncorrectIDExceptions
from src.domain.common.commands.base import BaseCommands
from src.infrastructure.db.services import (
    BaseCommandCarsMongoDBService,
    BaseCommandCarsParserMongoDBService,
    BaseQueryCarsMongoDBService,
    BaseQueryParserCarsMongoDBService,
)
from src.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class ParserCarsCommand(BaseCommands):
    offset: int


@dataclass(frozen=True)
class ParserCarsCommandHandler(CommandHandler[ParserCarsCommand, DTOCars]):
    query_pasring_all_cars_service: BaseQueryParserCarsMongoDBService
    command_save_cars_service: BaseCommandCarsParserMongoDBService

    async def handle(
        self,
        command: ParserCarsCommand,
    ) -> Dict:
        cars = await self.query_pasring_all_cars_service.parser_cars_all_cars(
            offset=command.offset,
        )
        original_cars = cars.copy()

        await self.command_save_cars_service.save_cars_from_parser(cars)

        return original_cars


@dataclass(frozen=True)
class GetAllCarsCommand(BaseCommands):
    offset: int


@dataclass(frozen=True)
class GetAllCarsCommandHandler(CommandHandler[GetAllCarsCommand, DTOCars]):
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
class GetCarByIdCommandHandler(CommandHandler[GetCarByIdCommand, DTOCars]):
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
class GetCarsByMarkCommandHandler(CommandHandler[GetCarsByMarkCommand, DTOCars]):
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
class GetCarsByYearCommandHandler(CommandHandler[GetCarsByYearCommand, DTOCars]):
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


@dataclass(frozen=True)
class DeletingCarByIDCommand(BaseCommands):
    car_id: str


@dataclass(frozen=True)
class DeletingCarByIDCommandHandler(CommandHandler[DeletingCarByIDCommand, DTOCars]):
    command_deleting_car_service: BaseCommandCarsMongoDBService

    async def handle(
        self,
        command: DeletingCarByIDCommand,
    ) -> bool:
        try:
            result = await self.command_deleting_car_service.delete_car_from_mongo(
                car_id=command.car_id,
            )
        except Exception:
            raise IncorrectIDExceptions()

        return result


@dataclass(frozen=True)
class CreatingCarCommand(BaseCommands):
    car_schema: DTOCars


@dataclass(frozen=True)
class CreatingCarCommandHandler(CommandHandler[CreatingCarCommand, DTOCars]):
    command_creating_car_service: BaseCommandCarsMongoDBService

    async def handle(
        self,
        command: CreatingCarCommand,
    ) -> bool:
        await self.command_creating_car_service.save_car_from_user(
            car=command.car_schema.to_dict(),
        )


@dataclass(frozen=True)
class PuttingCarCommand(BaseCommands):
    car_id: str
    car_data: CarUpdateSchema


@dataclass(frozen=True)
class PuttingCarCommandHandler(CommandHandler[PuttingCarCommand, DTOCars]):
    query_putting_car_service: BaseQueryCarsMongoDBService
    command_putting_car_service: BaseCommandCarsMongoDBService

    async def handle(
        self,
        command: PuttingCarCommand,
    ) -> bool:
        is_car_existing = await self.query_putting_car_service.get_car_by_id(
            id_car=command.car_id,
        )

        if not is_car_existing:
            raise HTTPException(status_code=400, detail="Object Not Exist.")

        update_fields = self.get_real_update_fields(command.car_data)
        if not update_fields:
            # If nothing to update
            raise HTTPException(status_code=400, detail="No Data For Update.")

        await self.command_putting_car_service.putting_car_mongo(
            car_id=command.car_id,
            car_data=update_fields,
        )

    @staticmethod
    def get_real_update_fields(car_data: CarUpdateSchema) -> dict:
        return {
            k: v for k, v in car_data.dict().items() if v not in [None, "string", 0]
        }
