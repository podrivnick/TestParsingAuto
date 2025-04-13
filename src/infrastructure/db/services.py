from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Dict,
    List,
)


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

    @abstractmethod
    async def get_car_by_id(self, id_car: str) -> Dict:
        raise NotImplementedError()

    @abstractmethod
    async def get_cars_by_mark(self, mark: str) -> List[Dict]:
        raise NotImplementedError()

    @abstractmethod
    async def get_cars_by_year(self, year: int) -> List[Dict]:
        raise NotImplementedError()

    @abstractmethod
    async def filter_cars(
        self,
        year: int,
        price: str,
        mileage: str,
    ) -> List[Dict]:
        raise NotImplementedError()


@dataclass
class BaseCommandCarsMongoDBService(ABC):
    @abstractmethod
    async def save_car_from_user(self, cars: Dict) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_car_from_mongo(self, car_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def putting_car_mongo(
        self,
        car_id: str,
        car_data: Dict,
    ) -> None:
        raise NotImplementedError()


@dataclass
class BaseCommandCarsParserMongoDBService(ABC):
    @abstractmethod
    async def save_cars_from_parser(self, cars: Dict) -> None:
        raise NotImplementedError()
