from typing import List

from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from punq import Container
from src.application.cars.commands.cars import (
    GetAllCarsCommand,
    GetCarByIdCommand,
    GetCarsByMarkCommand,
    GetCarsByYearCommand,
    ParserCarsCommand,
)
from src.application.cars.dto.car import DTOAllCars
from src.application.cars.schemas.base import CarSchema
from src.domain.common.exceptions.base import BaseAppException
from src.infrastructure.di.main import init_container
from src.infrastructure.mediator.main import Mediator
from src.presentation.api.controllers.responses.base import (
    ErrorData,
    SuccessResponse,
)
from src.presentation.api.providers.stub import Stub


router = APIRouter(tags=["Auto Galery"])


@router.get(
    "/sync",
    status_code=status.HTTP_201_CREATED,
    description="API Parser All Cars From OLX",
    responses={
        status.HTTP_201_CREATED: {"model": DTOAllCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def parsing_cars_handler(
    offset: int,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[DTOAllCars]]:
    """Parsing Cars."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        cars = await mediator.handle_command(
            ParserCarsCommand(offset=offset),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return SuccessResponse(result=cars)


@router.get(
    "/cars",
    status_code=status.HTTP_201_CREATED,
    description="API for getting all machines using parsing",
    responses={
        status.HTTP_201_CREATED: {"model": DTOAllCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def get_all_cars_handler(
    offset: int,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Receiving All Cars."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        cars = await mediator.handle_command(
            GetAllCarsCommand(offset=offset),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return SuccessResponse(result=cars)


@router.get(
    "/cars_id",
    status_code=status.HTTP_201_CREATED,
    description="API for getting car by id",
    responses={
        status.HTTP_201_CREATED: {"model": DTOAllCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def get_car_by_id_handler(
    id_car: str,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Receiving Car by ID."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        cars = await mediator.handle_command(
            GetCarByIdCommand(id_car=id_car),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return SuccessResponse(result=cars)


@router.get(
    "/cars_mark",
    status_code=status.HTTP_201_CREATED,
    description="API for getting cars by mark",
    responses={
        status.HTTP_201_CREATED: {"model": DTOAllCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def get_cars_by_mark_handler(
    mark: str,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Receiving Cars by Mark."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        cars = await mediator.handle_command(
            GetCarsByMarkCommand(mark=mark),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return SuccessResponse(result=cars)


@router.get(
    "/cars_year",
    status_code=status.HTTP_201_CREATED,
    description="API for getting cars by year",
    responses={
        status.HTTP_201_CREATED: {"model": DTOAllCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def get_car_by_year_handler(
    year: int,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Receiving Cars by Year."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        cars = await mediator.handle_command(
            GetCarsByYearCommand(year=year),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return SuccessResponse(result=cars)
