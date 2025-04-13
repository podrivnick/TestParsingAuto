from dataclasses import dataclass
from typing import ClassVar

from src.domain.common.exceptions.base import BaseAppException


@dataclass(eq=False)
class BaseMediatorException(BaseAppException):
    @property
    def message(self) -> str:
        return "Error while check request"


@dataclass(eq=False)
class BaseAppException(Exception):
    """Base class for app exceptions."""

    status: ClassVar[int] = 500

    @property
    def message(self) -> str:
        return "Some Exception in App"


@dataclass(eq=False)
class DomainException(BaseAppException):
    """Base class for domain exceptions."""

    @property
    def message(self) -> str:
        return "Domain exception occured"
