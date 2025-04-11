from dataclasses import dataclass

from src.domain.common.exceptions.base import BaseAppException


@dataclass(eq=False)
class BaseMediatorException(BaseAppException):
    @property
    def message(self) -> str:
        return "Error while check request"
