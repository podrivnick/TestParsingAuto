from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException


@dataclass(eq=False)
class BaseArtException(ValueError, DomainException):
    @property
    def message(self):
        return "Invalid Art"


@dataclass(eq=False)
class ArtIsNotExistException(BaseArtException):
    @property
    def message(self):
        return "Art is not exist"
