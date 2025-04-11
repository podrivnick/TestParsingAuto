from dataclasses import dataclass

from src.domain.arts.exceptions.art import ArtIsNotExistException
from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class Art(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if not self.exists():
            raise ArtIsNotExistException()

    def exists(self) -> bool:
        return self.value is not None
