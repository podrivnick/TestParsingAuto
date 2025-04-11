from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from punq import Container
from src.application.arts.commands.arts import GetRandomArtCommand
from src.application.arts.dto.art import DTOArt
from src.application.arts.schemas.base import GetRandomArtSchema
from src.application.flowers.commands.flowers import GetRandomFlowerCommand
from src.application.flowers.dto.flower import DTOFlower
from src.application.flowers.schemas.base import GetRandomFlowerSchema
from src.application.poems.commands.poems import GetRandomPoemCommand
from src.application.poems.dto.poem import DTOPoem
from src.application.poems.schemas.base import GetRandomPoemByCertainAuthorSchema
from src.domain.common.exceptions.base import BaseAppException
from src.infrastructure.di.main import init_container
from src.infrastructure.mediator.main import Mediator
from src.presentation.api.controllers.responses.base import (
    ErrorData,
    SuccessResponse,
)
from src.presentation.api.providers.stub import Stub


router = APIRouter(tags=["Galery"])


@router.post(
    "/random_art",
    status_code=status.HTTP_201_CREATED,
    description="Апи для получения случайной картины",
    responses={
        status.HTTP_201_CREATED: {"model": DTOArt},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def get_random_art_handler(
    schema: GetRandomArtSchema,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[DTOArt]:
    """Получить случайную картину из введённой категории."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        art = await mediator.handle_command(
            GetRandomArtCommand(art_direction=schema.art_direction),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return SuccessResponse(result=art)
