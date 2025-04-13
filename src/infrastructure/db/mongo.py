from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

import anyio
from bson import ObjectId
from src.domain.cars.exceptions.car import AlreadyExistOblectExceptions
from src.infrastructure.db.config import BaseMongoDBRepository
from src.infrastructure.db.services import (
    BaseCommandCarsMongoDBService,
    BaseCommandCarsParserMongoDBService,
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
        cursor = self._collection.find().limit(offset)
        result = [doc async for doc in cursor]

        return result

    async def get_car_by_id(
        self,
        id_car: str,
    ) -> Dict:
        try:
            obj_id = ObjectId(id_car)
        except Exception:
            return None

        document = await self._collection.find_one({"_id": obj_id})
        return document

    async def get_cars_by_mark(
        self,
        mark: str,
    ) -> List[Dict]:
        cursor = self._collection.find(
            {
                "mark": {"$regex": mark, "$options": "i"},
            },
        )

        results = []
        async for doc in cursor:
            results.append(doc)

        return results

    async def get_cars_by_year(
        self,
        year: int,
    ) -> List[Dict]:
        cursor = self._collection.find({"year_created": int(year)})

        results = []
        async for doc in cursor:
            results.append(doc)

        return results


@dataclass
class CommandCarsMongoDBService(BaseCommandCarsMongoDBService, BaseMongoDBRepository):
    async def save_car_from_user(
        self,
        car: Dict,
    ) -> None:
        """Зберігає список машин від користувача MongoDB.

        Викидає AlreadyExistObjectExceptions, якщо об'єкт вже існує.
        """
        result = await self._collection.update_one(
            car,
            {"$set": car},
            upsert=True,
        )

        raw = result.raw_result
        if raw.get("updatedExisting", False) is True:
            raise AlreadyExistOblectExceptions(
                "Car already exists with identical fields.",
            )

    async def delete_car_from_mongo(
        self,
        car_id: str,
    ) -> None:
        obj_id = ObjectId(car_id)

        result = await self._collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0

    async def putting_car_mongo(
        self,
        car_id: str,
        car_data: Dict,
    ) -> None:
        obj_id = ObjectId(car_id)

        await self._collection.update_one(
            {"_id": obj_id},
            {"$set": car_data},
            upsert=False,
        )


@dataclass
class CommandCarsParserMongoDBService(
    BaseCommandCarsParserMongoDBService,
    BaseMongoDBRepository,
):
    async def save_cars_from_parser(
        self,
        car_list: List,
    ) -> None:
        for car in car_list:
            await self._collection.update_one(
                car,
                {"$set": car},
                upsert=True,
            )
