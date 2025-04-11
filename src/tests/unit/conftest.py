from punq import Container
from pytest import fixture
from src.infrastructure.db.services import (
    BaseArtMongoDBService,
    BaseFlowerMongoDBService,
    BasePoemMongoDBService,
)
from src.infrastructure.mediator.main import Mediator
from src.tests.unit.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def art_service(container: Container) -> BaseArtMongoDBService:
    return container.resolve(BaseArtMongoDBService)


@fixture()
def flower_service(container: Container) -> BaseFlowerMongoDBService:
    return container.resolve(BaseFlowerMongoDBService)


@fixture()
def poem_service(container: Container) -> BasePoemMongoDBService:
    return container.resolve(BasePoemMongoDBService)
