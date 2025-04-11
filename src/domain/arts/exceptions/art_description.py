from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException


@dataclass(eq=False)
class BaseArtDescriptionNameException(ValueError, DomainException):
    @property
    def message(self):
        return "Invalid Art Description"


@dataclass(eq=False)
class ArtDescriptionIsNotExistException(BaseArtDescriptionNameException):
    @property
    def message(self):
        return "Art Description is not exist"
