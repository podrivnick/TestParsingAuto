from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Optional,
)

from bson import ObjectId
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)
from src.infrastructure.parser.utils import (
    parse_mileage,
    parse_price,
)


def str_objectid(obj: ObjectId) -> str:
    return str(obj)


@dataclass(frozen=True, eq=False)
class CarSchema:
    _id: Optional[str] = field(default=None)
    mark: Optional[str] = field(default=None)
    model: Optional[str] = field(default=None)
    year_created: Optional[int] = field(default=None)
    price: Optional[float] = field(default=None)
    mileage: Optional[int] = field(default=None)
    engine_type: Optional[str] = field(default=None)
    engine_capacity: Optional[float] = field(default=None)
    gear_box: Optional[str] = field(default=None)
    drive_type: Optional[str] = field(default=None)
    location: Optional[str] = field(default=None)
    url_image: Optional[str] = field(default=None)
    mileage_numeric: Optional[int] = field(default=None)
    price_numeric: Optional[int] = field(default=None)

    def __post_init__(self):
        if isinstance(self._id, ObjectId):
            object.__setattr__(self, "_id", str(self._id))

    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "brand": self.brand,
            "model": self.model,
            "year_created": self.year_created,
            "price": self.price,
            "mileage": self.mileage,
            "engine_type": self.engine_type,
            "engine_capacity": self.engine_capacity,
            "drive_type": self.drive_type,
            "location": self.location,
            "url_image": self.url_image,
            "gear_box": self.gear_box,
            "mileage_numeric": self.gear_box,
            "price_numeric": self.gear_box,
        }


class CarUpdateSchema(BaseModel):
    price: str = Field(
        default="0 $",
        pattern=r"^\d+(?:\s\d+)*\s*\$$",
        description="Ціна автомобіля. Приклад: '3 099 $'. Значення за замовчуванням: '0 $'",
    )
    mileage: str = Field(
        default="0 тис.км.",
        pattern=r"^\d+(?:\s\d+)*\s*(?:тис\.?\s*км\.?)$",
        description="Пробіг автомобіля. Приклад: '480 тис.км.'. Значення за умовчанням: '0 тис.км.'",
    )
    mark: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)
    year_created: Optional[int] = Field(default=None)
    engine_type: Optional[str] = Field(default=None)
    engine_capacity: Optional[float] = Field(default=None)
    gear_box: Optional[str] = Field(default=None)
    drive_type: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    url_image: Optional[str] = Field(default=None)

    price_numeric: Optional[int] = None
    mileage_numeric: Optional[int] = None

    @model_validator(mode="after")
    def compute_numeric_fields(self) -> "CarUpdateSchema":
        if self.price != "0 $":
            self.price_numeric = parse_price(self.price)

        if self.mileage != "0 тис.км.":
            self.mileage_numeric = parse_mileage(self.mileage)

        return self
