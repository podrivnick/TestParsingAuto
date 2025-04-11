from typing import (
    Any,
    Mapping,
)

from src.domain.arts import value_objects as art_vo
from src.domain.arts.entities.art import Art
from src.domain.flowers import value_objects as flower_vo
from src.domain.flowers.entities.flower import Flower
from src.domain.poems import value_objects as poem_vo
from src.domain.poems.entities.poem import Poem


def convert_art_document_to_entity(message_document: Mapping[str, Any]) -> Art:
    return Art.create_art(
        art=art_vo.Art(message_document["art"]),
        art_name=art_vo.ArtName(message_document["art_name"]),
        art_direction=art_vo.ArtDirection(message_document["art_direction"]),
        art_description=art_vo.ArtDescription(message_document["art_description"]),
    )
