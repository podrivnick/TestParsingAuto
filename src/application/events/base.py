from abc import ABC
from dataclasses import dataclass
from typing import TypeVar

from src.domain.common.events.base import BaseEvent


ET = TypeVar("ET", bound=BaseEvent)


@dataclass
class IntegrationEvent(BaseEvent, ABC):
    pass
