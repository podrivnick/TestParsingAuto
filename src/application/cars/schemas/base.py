from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Optional,
)

from bson import ObjectId


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
        }
