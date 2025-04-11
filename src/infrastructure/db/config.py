from abc import ABC
from dataclasses import dataclass
from typing import List

from motor.core import AgnosticClient


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection: str

    @property
    def _collection(self) -> str:
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection]
