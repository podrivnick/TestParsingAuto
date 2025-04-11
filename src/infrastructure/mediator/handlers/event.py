from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from src.domain.common.events.base import BaseEvent
from src.infrastructure.message_broker.base import BaseMessageBroker


ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = None

    @abstractmethod
    def handle(self, event: ET) -> ER:
        raise NotImplementedError()
