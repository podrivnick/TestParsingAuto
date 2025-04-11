from dataclasses import dataclass


@dataclass(frozen=True)
class DTOArt:
    art: str
    art_name: str
    art_direction: str
    art_description: str
