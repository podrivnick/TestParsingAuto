from dataclasses import dataclass

from src.domain.arts import value_objects as vo
from src.domain.arts.entities.art import Art
from src.domain.common.commands.base import BaseCommands
from src.infrastructure.db.services import BaseArtMongoDBService
from src.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class GetRandomArtCommand(BaseCommands):
    art_direction: str


@dataclass(frozen=True)
class GetRandomArtCommandHandler(CommandHandler[GetRandomArtCommand, Art]):
    arts_service: BaseArtMongoDBService

    async def handle(
        self,
        command: GetRandomArtCommand,
    ) -> Art:
        art_direction = vo.ArtDirection(command.art_direction)

        art = await self.arts_service.get_random_art(art_direction.to_raw())

        await self._mediator.publish_event(art.pull_events())

        return art
