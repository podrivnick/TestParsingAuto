from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException


@dataclass(eq=False)
class BaseArtDirectionException(ValueError, DomainException):
    @property
    def message(self):
        return "Invalid Art Direction"


@dataclass(eq=False)
class ArtDirectionIsEmptyException(BaseArtDirectionException):
    @property
    def message(self):
        return "Art Direction is empty"


@dataclass(eq=False)
class ArtDirectionInCorrectFormatException(BaseArtDirectionException):
    @property
    def message(self):
        return "Art Direction is incorrect format"


@dataclass(eq=False)
class ArtDirectionIsTooLongException(BaseArtDirectionException):
    @property
    def message(self):
        return "Art Direction is too long"
