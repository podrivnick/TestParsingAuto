import logging
from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import uuid4

from src.domain.common.entities import Entity
from src.domain.common.events.base import BaseEvent


@dataclass
class AggregateRoot(Entity, ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    _events: list[BaseEvent] = field(
        default_factory=list,
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "Entity") -> bool:
        return self.oid == __value.oid

    def record_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def get_events(self) -> list[BaseEvent]:
        return self._events

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> list[BaseEvent]:
        events = self.get_events().copy()
        logging.info(f"Код дошел до aggregate {self._events}")
        self.clear_events()
        return events
