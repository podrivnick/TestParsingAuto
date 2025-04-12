from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Dict


@dataclass
class BaseQueryParserCarsMongoDBService(ABC):
    @abstractmethod
    async def parser_cars_all_cars(self, offset: int) -> None:
        raise NotImplementedError()


@dataclass
class BaseQueryCarsMongoDBService(ABC):
    @abstractmethod
    async def get_all_cars(self, offset: int) -> Dict:
        raise NotImplementedError()


@dataclass
class BaseCommandCarsMongoDBService(ABC):
    @abstractmethod
    async def save_cars_to_mongo(self, cars: Dict) -> None:
        raise NotImplementedError()
