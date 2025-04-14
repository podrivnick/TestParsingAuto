from typing import List

from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from punq import Container
from src.application.cars.commands.cars import (
    CreatingCarCommand,
    DeletingCarByIDCommand,
    FilterCarsCommand,
    GetAllCarsCommand,
    GetCarByIdCommand,
    GetCarsByMarkCommand,
    GetCarsByYearCommand,
    ParserCarsCommand,
    PuttingCarCommand,
)
from src.application.cars.dto.car import DTOCars
from src.application.cars.schemas.base import (
    CarSchema,
    CarUpdateSchema,
)
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
    description="API Parser All Cars From OLX. RECOMMEND SET 'OFFSET'=1 FOR NOT WAITING TOO LONG",
    responses={
        status.HTTP_201_CREATED: {"model": DTOCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def parsing_cars_handler(
    offset: int,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[DTOCars]]:
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
        status.HTTP_201_CREATED: {"model": DTOCars},
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
        status.HTTP_201_CREATED: {"model": DTOCars},
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
        status.HTTP_201_CREATED: {"model": DTOCars},
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
        status.HTTP_201_CREATED: {"model": DTOCars},
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


@router.delete(
    "/car_delete",
    status_code=status.HTTP_201_CREATED,
    description="API deleting car by ID",
    responses={
        status.HTTP_201_CREATED: {"model": DTOCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def delete_car_by_id_handler(
    car_id: str,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Deleting Car By ID."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        is_car_deleted = await mediator.handle_command(
            DeletingCarByIDCommand(car_id=car_id),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    if is_car_deleted:
        return SuccessResponse(result="Car Succesfully Deleted")


@router.post(
    "/car_create",
    status_code=status.HTTP_201_CREATED,
    description="API creating car",
    responses={
        status.HTTP_201_CREATED: {"model": DTOCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def create_car_handler(
    car_schema: DTOCars,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Creating Car."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        is_car_created = await mediator.handle_command(
            CreatingCarCommand(car_schema=car_schema),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    if is_car_created:
        return SuccessResponse(result="Car Succesfully Added")


@router.put(
    "/car_put",
    status_code=status.HTTP_201_CREATED,
    description="API creating car",
    responses={
        status.HTTP_201_CREATED: {"model": DTOCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def put_car_handler(
    car_id: str,
    car_data: CarUpdateSchema,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Creating Car."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        is_car_putted = await mediator.handle_command(
            PuttingCarCommand(
                car_id=car_id,
                car_data=car_data,
            ),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    if is_car_putted:
        return SuccessResponse(result="Car Succesfully Changed")


@router.get(
    "/cars_filter",
    status_code=status.HTTP_201_CREATED,
    description="API for filter cars",
    responses={
        status.HTTP_201_CREATED: {"model": DTOCars},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorData},
    },
)
async def filter_cars_handler(
    less_price: int,
    larger_year: int,
    larger_mileage: int,
    container: Container = Depends(Stub(init_container)),
) -> SuccessResponse[List[CarSchema]]:
    """Filtering Cars."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        cars = await mediator.handle_command(
            FilterCarsCommand(
                price=less_price,
                year=larger_year,
                mileage=larger_mileage,
            ),
        )
    except BaseAppException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return SuccessResponse(result=cars)
