from dataclasses import dataclass

from src.domain.arts.exceptions.art_name import (
    ArtNameIsEmptyException,
    ArtNameTooLongException,
)
from src.domain.common.value_objects.base import ValueObject


MAX_ART_NAME_LENGTH = 40


@dataclass(frozen=True)
class ArtName(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if len(self.value) == 0:
            raise ArtNameIsEmptyException()

        if len(self.value) > MAX_ART_NAME_LENGTH:
            raise ArtNameTooLongException()

    def exists(self) -> bool:
        return self.value is not None
