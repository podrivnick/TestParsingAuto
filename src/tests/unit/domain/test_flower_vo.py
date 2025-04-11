import pytest
from src.domain.flowers import (
    exceptions as ex,
    value_objects as flower_vo,
)
from src.domain.flowers.entities.flower import Flower


def test_flower_name_is_valid():
    flowe_name_empty = ""
    flower_name_is_too_long = "fdsdf3"
    flower_name_is_incorrect_format = "~~fsfsdf33r34ASDA"

    with pytest.raises(ex.FlowerNameIsEmptyException):
        flower_vo.FlowerName(flowe_name_empty)

    with pytest.raises(ex.FlowerNameIsTooLongException):
        flower_vo.FlowerName(flower_name_is_too_long * 200)

    with pytest.raises(ex.FlowerNameInCorrectFormatException):
        flower_vo.FlowerName(flower_name_is_incorrect_format)


def test_flower_path_is_valid():
    flowe_path_empty = ""
    flower_path_is_too_long = "fdsdf3"
    flower_path_is_incorrect_format = "~~fsfsdf33r34ASDA"

    with pytest.raises(ex.FlowerPathIsEmptyException):
        flower_vo.FlowerPath(flowe_path_empty)

    with pytest.raises(ex.FlowerPathIsTooLongException):
        flower_vo.FlowerPath(flower_path_is_too_long * 200)

    with pytest.raises(ex.FlowerPathInCorrectFormatException):
        flower_vo.FlowerPath(flower_path_is_incorrect_format)


def test_flower_entity_is_valid():
    flower_name = flower_vo.FlowerName("Roza")
    flower_path = flower_vo.FlowerPath("../sd/a")

    flower = Flower.create_flower(
        flower_name=flower_name,
        flower_path=flower_path,
    )

    assert flower.flower_name == flower_name
    assert flower.flower_path == flower_path
