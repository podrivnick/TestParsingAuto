import re
from dataclasses import dataclass

from src.domain.arts.exceptions.art_direction import (
    ArtDirectionInCorrectFormatException,
    ArtDirectionIsEmptyException,
    ArtDirectionIsTooLongException,
)
from src.domain.common.value_objects.base import ValueObject


MAX_ART_DIRECTION_LENGTH = 40
ART_DIRECTION_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(frozen=True)
class ArtDirection(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if len(self.value) == 0:
            raise ArtDirectionIsEmptyException()

        if len(self.value) > MAX_ART_DIRECTION_LENGTH:
            raise ArtDirectionIsTooLongException()

        if not ART_DIRECTION_PATTERN.match(self.value):
            raise ArtDirectionInCorrectFormatException()

    def exists(self) -> bool:
        return self.value is not None
