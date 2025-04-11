import random
from dataclasses import (
    dataclass,
    field,
)
from typing import List

from src.domain.arts.entities.art import Art
from src.domain.flowers.entities.flower import Flower
from src.domain.poems.entities.poem import Poem
from src.infrastructure.db.config import (
    get_saved_arts,
    get_saved_flowers,
    get_saved_poems,
)
from src.infrastructure.db.convertors import (
    convert_art_document_to_entity,
    convert_flower_document_to_entity,
    convert_poem_document_to_entity,
)
from src.infrastructure.db.services import (
    BaseArtMongoDBService,
    BaseFlowerMongoDBService,
    BasePoemMongoDBService,
)


@dataclass
class ArtMongoDummyService(BaseArtMongoDBService):
    _saved_arts: List[dict] = field(default_factory=list, kw_only=True)

    def __post_init__(self):
        self._saved_arts = get_saved_arts()

    async def get_random_art(
        self,
        art_direction: str,
    ) -> Art:
        filtered_arts = list(
            filter(
                lambda art: art.get("art_direction") == art_direction,
                self._saved_arts,
            ),
        )

        random_art = random.choice(filtered_arts) if filtered_arts else None  # noqa DUO102

        return convert_art_document_to_entity(random_art) if random_art else None
