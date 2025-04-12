from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

import anyio
from src.infrastructure.db.config import BaseMongoDBRepository
from src.infrastructure.db.services import (
    BaseCommandCarsMongoDBService,
    BaseQueryCarsMongoDBService,
    BaseQueryParserCarsMongoDBService,
)
from src.infrastructure.parser.parser_auto import parsing_olx_cars


@dataclass
class QueryParserCarsMongoDBService(BaseQueryParserCarsMongoDBService):
    async def parser_cars_all_cars(
        self,
        offset: int,
    ) -> Dict:
        cars = await anyio.to_thread.run_sync(
            parsing_olx_cars,
            offset,
        )

        return cars


@dataclass
class QueryCarsMongoDBService(BaseQueryCarsMongoDBService, BaseMongoDBRepository):
    async def get_all_cars(
        self,
        offset: int,
    ) -> Dict:
        # TODO
        cursor = self._collection.find().limit(offset)
        result = [doc async for doc in cursor]

        return result


@dataclass
class CommandCarsMongoDBService(BaseCommandCarsMongoDBService, BaseMongoDBRepository):
    async def save_cars_to_mongo(
        self,
        car_list: List,
    ) -> None:
        for car in car_list:
            self._collection.update_one(
                car,
                {"$set": car},
                upsert=True,
            )
