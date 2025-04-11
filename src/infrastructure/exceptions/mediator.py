from dataclasses import dataclass

from src.infrastructure.exceptions.base import BaseMediatorException


@dataclass(eq=False)
class EventHandlerNotRegisteredException(BaseMediatorException):
    @property
    def message(self) -> str:
        return "Event handler not registered for the given event"


@dataclass(eq=False)
class CommandHandlerNotRegisteredException(BaseMediatorException):
    @property
    def message(self) -> str:
        return "Command handler not registered for the given event"
