from dataclasses import (
    dataclass,
    field,
)


@dataclass
class APIConfig:
    port: int = 8000
    host: str = "0.0.0.0"
    debug: bool = __debug__


@dataclass
class MConfig:
    api: APIConfig = field(default_factory=APIConfig)
