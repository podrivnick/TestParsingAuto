from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import ClassVar
from uuid import uuid4


@dataclass
class BaseEvent(ABC):
    title: ClassVar[str]

    event_id: str = field(kw_only=True, default_factory=lambda: str(uuid4()))
    event_timestamp: datetime = field(
        kw_only=True,
        default_factory=datetime.utcnow,
    )
