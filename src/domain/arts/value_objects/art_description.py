from dataclasses import dataclass

from src.domain.arts.exceptions.art_description import ArtDescriptionIsNotExistException
from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class ArtDescription(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if not self.exists():
            raise ArtDescriptionIsNotExistException()

    def exists(self) -> bool:
        return self.value is not None
