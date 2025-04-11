from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    @abstractmethod
    async def send_message(self, key: str, topic: str, value: dict):
        raise NotImplementedError()

    @abstractmethod
    async def start_consuming(self, topic: str):
        raise NotImplementedError()

    @abstractmethod
    async def stop_consuming(self, topic: str):
        raise NotImplementedError()
