from typing import (
    Dict,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)
from src.infrastructure.parser.utils import (
    parse_mileage,
    parse_price,
)


class DTOCars(BaseModel):
    price: str = Field(
        default="0 $",
        pattern=r"^\d+(?:\s\d+)*\s*\$$",
        description="Ціна автомобіля. Приклад: '3 099 $'. Значення за замовчуванням: '0$'",
    )
    mileage: str = Field(
        default="0 тис.км.",
        pattern=r"^\d+(?:\s\d+)*\s*(?:тис\.?\s*км\.?)$",
        description="Пробіг автомобіля. Приклад: '480 тис.км.'. Значення за умовчанням: '0 тис.км.'",
    )
    mark: Optional[str] = Field(default=None, description="Марка автомобіля")
    model: Optional[str] = Field(default=None, description="Модель автомобіля")
    year_created: Optional[int] = Field(default=None, description="Рік випуску")
    engine_type: Optional[str] = Field(default=None, description="Тип двигуна")
    engine_capacity: Optional[str] = Field(default=None, description="Об'єм двигуна")
    gear_box: Optional[str] = Field(default=None, description="Коробка передач")
    drive_type: Optional[str] = Field(default=None, description="Тип приводу")
    location: Optional[str] = Field(default=None, description="Локація")
    url_image: Optional[str] = Field(
        default=None,
        description="Посилання на зображення",
    )

    def to_dict(self) -> Dict:
        return {
            "mark": self.mark,
            "model": self.model,
            "year_created": self.year_created,
            "price": self.price,
            "mileage": self.mileage,
            "engine_type": self.engine_type,
            "engine_capacity": self.engine_capacity,
            "drive_type": self.drive_type,
            "location": self.location,
            "url_image": self.url_image,
            "price_numeric": parse_price(self.price),
            "mileage_numeric": parse_mileage(self.mileage),
            "gear_box": self.gear_box,
        }
