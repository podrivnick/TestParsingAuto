from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from src.domain.common.events.base import BaseEvent
from src.infrastructure.mediator.handlers.event import (
    ER,
    ET,
    EventHandler,
)


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_events(
        self,
        event: ET,
        event_handlers: Iterable[EventHandler[ET, ER]],
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def publish_event(
        self,
        events: Iterable[BaseEvent],
    ) -> Iterable[ER]:
        raise NotImplementedError()
