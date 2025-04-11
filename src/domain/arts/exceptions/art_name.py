from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException


@dataclass(eq=False)
class BaseArtNameException(ValueError, DomainException):
    @property
    def message(self):
        return "Invalid Art Name"


@dataclass(eq=False)
class ArtNameTooLongException(BaseArtNameException):
    @property
    def message(self):
        return "Art Name is too long"


@dataclass(eq=False)
class ArtNameIsEmptyException(BaseArtNameException):
    @property
    def message(self):
        return "Art Name can't be empty"
