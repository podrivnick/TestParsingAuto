from dataclasses import dataclass


@dataclass(frozen=True)
class GetRandomArtSchema:
    art_direction: str
