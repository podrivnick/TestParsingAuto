from dataclasses import dataclass
from typing import ClassVar

from src.application.arts.events.base import IntegrationEvent
from src.domain.arts.events.arts import GetRandomArtEvent
from src.infrastructure.mediator.handlers.event import EventHandler
from src.infrastructure.message_broker.convertors import convert_event_to_broker_message


@dataclass
class GetRandomArtEventHandler(EventHandler[GetRandomArtEvent, None]):
    async def handle(self, event: GetRandomArtEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )


@dataclass
class ArtReceivedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = "Random Art Recieved Event"

    art: str
    art_name: str
    art_direction: str
    art_description: str


@dataclass
class ArtReceivedFromBrokerEventHandler(EventHandler[ArtReceivedFromBrokerEvent, None]):
    async def handle(self, event: ArtReceivedFromBrokerEvent) -> None:
        await self.connection_manager.send_all(
            key=event.chat_oid,
            bytes_=convert_event_to_broker_message(event=event),
        )
