from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from src.infrastructure.exceptions.base import DomainException


@dataclass(eq=False)
class BaseCarException(ValueError, DomainException):
    @property
    def message(self):
        return "Invalid Car Data"


@dataclass(eq=False)
class IncorrectIDExceptions(BaseCarException):
    exception: Optional[str] = field(default="Incorrect ID")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(eq=False)
class AlreadyExistOblectExceptions(BaseCarException):
    exception: Optional[str] = field(default="Car Already In DataBase")

    @property
    def message(self) -> Optional[str]:
        return self.exception
