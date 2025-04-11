from punq import (
    Container,
    Scope,
)
from src.infrastructure.db.dummy_services import (
    ArtMongoDummyService,
    FlowerMongoDummyService,
    PoemMongoDummyService,
)
from src.infrastructure.db.services import (
    BaseArtMongoDBService,
    BaseFlowerMongoDBService,
    BasePoemMongoDBService,
)
from src.infrastructure.di.main import _initialize_container


def init_dummy_container() -> Container:
    container = _initialize_container()
    container.register(
        BaseArtMongoDBService,
        ArtMongoDummyService,
        scope=Scope.singleton,
    )
    container.register(
        BaseFlowerMongoDBService,
        FlowerMongoDummyService,
        scope=Scope.singleton,
    )
    container.register(
        BasePoemMongoDBService,
        PoemMongoDummyService,
        scope=Scope.singleton,
    )

    return container
