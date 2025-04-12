from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Optional,
)


@dataclass(frozen=True)
class DTOAllCars:
    mark: Optional[str] = field(default=None)
    price: Optional[float] = field(default=None)
    mileage: Optional[int] = field(default=None)
    model: Optional[str] = field(default=None)
    year_created: Optional[int] = field(default=None)
    engine_type: Optional[str] = field(default=None)
    gear_box: Optional[str] = field(default=None)
    drive_type: Optional[str] = field(default=None)
    engine_capacity: Optional[float] = field(default=None)
    location: Optional[str] = field(default=None)
    url_image: Optional[str] = field(default=None)

    def to_dict(self) -> Dict:
        return {
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
        }
