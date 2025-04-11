from dataclasses import dataclass
from typing import ClassVar

from src.domain.common.events.base import BaseEvent


@dataclass
class GetRandomArtEvent(BaseEvent):
    event_title: ClassVar[str] = "Random Art Recieved Event"

    art: str
    art_name: str
    art_direction: str
    art_description: str
