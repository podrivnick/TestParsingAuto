from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from src.domain.common.commands.base import BaseCommands
from src.domain.common.events.base import BaseEvent
from src.infrastructure.exceptions.mediator import (
    CommandHandlerNotRegisteredException,
    EventHandlerNotRegisteredException,
)
from src.infrastructure.mediator.handlers.commands import (
    CommandHandler,
    CR,
    CT,
)
from src.infrastructure.mediator.handlers.event import (
    ER,
    ET,
    EventHandler,
)
from src.infrastructure.mediator.sub_mediators.commands import CommandMediator
from src.infrastructure.mediator.sub_mediators.event import EventMediator


@dataclass(eq=False)
class Mediator(EventMediator, CommandMediator):
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CR, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_events(
        self,
        event: ET,
        event_handlers: Iterable[EventHandler[ET, ER]],
    ) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(
        self,
        command: CT,
        command_handlers: Iterable[CommandHandler[CT, CR]],
    ) -> None:
        self.commands_map[command].extend(command_handlers)

    async def publish_event(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        results = []

        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[event.__class__]
            if not handlers:
                raise EventHandlerNotRegisteredException()

            results.extend([await handler.handle(event) for handler in handlers])

        return results

    async def handle_command(self, command: BaseCommands) -> Iterable[CR]:
        event_type = command.__class__
        handlers = self.commands_map.get(event_type)

        if not handlers:
            raise CommandHandlerNotRegisteredException()

        return [await handler.handle(command) for handler in handlers]
