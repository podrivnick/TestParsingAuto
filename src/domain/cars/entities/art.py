from dataclasses import dataclass
from typing import Self

from src.domain.arts import value_objects as vo
from src.domain.arts.events.arts import GetRandomArtEvent
from src.domain.common.entities.aggregate_root import AggregateRoot


@dataclass
class Art(AggregateRoot):
    art: vo.Art
    art_name: vo.ArtName
    art_direction: vo.ArtDirection
    art_description: vo.ArtDescription

    @classmethod
    def create_art(
        cls,
        art: vo.Art,
        art_name: vo.ArtName,
        art_direction: vo.ArtDirection,
        art_description: vo.ArtDescription,
    ) -> Self:
        art = cls(
            art=art,
            art_name=art_name,
            art_direction=art_direction,
            art_description=art_description,
        )

        art.record_event(
            GetRandomArtEvent(
                art=art.art.to_raw(),
                art_name=art.art_name.to_raw(),
                art_direction=art.art_direction.to_raw(),
                art_description=art.art_description.to_raw(),
            ),
        )

        return art
