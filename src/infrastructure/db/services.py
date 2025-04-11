from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from src.domain.arts.entities.art import Art
from src.domain.flowers.entities.flower import Flower
from src.domain.poems.entities.poem import Poem


@dataclass
class BaseArtMongoDBService(ABC):
    @abstractmethod
    async def get_random_art(self, art_direction: str) -> Art:
        raise NotImplementedError()
