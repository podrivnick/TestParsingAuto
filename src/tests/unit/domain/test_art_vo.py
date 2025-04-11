import pytest
from src.domain.arts import (
    exceptions as ex,
    value_objects as art_vo,
)
from src.domain.arts.entities.art import Art


def test_art_is_valid():
    art_empty = None

    with pytest.raises(ex.ArtIsNotExistException):
        art_vo.Art(art_empty)


def test_art_name_is_valid():
    art_name_empty = ""
    art_name_is_too_long = "Jupiter"

    with pytest.raises(ex.ArtNameIsEmptyException):
        art_vo.ArtName(art_name_empty)

    with pytest.raises(ex.ArtNameTooLongException):
        art_vo.ArtName(art_name_is_too_long * 200)


def test_art_direction_is_valid():
    art_direction_empty = ""
    art_direction_is_too_long = "Jupiter" * 41
    art_direction_is_incorrecr_format = "@flower"

    with pytest.raises(ex.ArtDirectionIsEmptyException):
        art_vo.ArtDirection(art_direction_empty)

    with pytest.raises(ex.ArtDirectionIsTooLongException):
        art_vo.ArtDirection(art_direction_is_too_long)

    with pytest.raises(ex.ArtDirectionInCorrectFormatException):
        art_vo.ArtDirection(art_direction_is_incorrecr_format)


def test_art_description_is_valid():
    art_description_empty = None

    with pytest.raises(ex.ArtDescriptionIsNotExistException):
        art_vo.ArtDescription(art_description_empty)


def test_art_entity_is_valid():
    art_path = art_vo.Art("../sd/a")
    art_name = art_vo.ArtName("Jupiter")
    art_direction = art_vo.ArtDirection("Jupiter's Great Work")
    art_description = art_vo.ArtDescription("The Masterpieces of Karavadjo")

    art = Art.create_art(
        art=art_path,
        art_name=art_name,
        art_direction=art_direction,
        art_description=art_description,
    )

    assert art.art == art_path
    assert art.art_name == art_name
    assert art.art_direction == art_direction
    assert art.art_description == art_description
