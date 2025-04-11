import pytest
from src.domain.poems import (
    exceptions as ex,
    value_objects as poem_vo,
)
from src.domain.poems.entities.poem import Poem


def test_poem_title_is_valid():
    poem_title_empty = ""
    poem_title_is_too_long = "Onegin"
    poem_title_is_incorrect_format = "~Onegin"

    with pytest.raises(ex.PoemTitleIsEmptyException):
        poem_vo.PoemTitle(poem_title_empty)

    with pytest.raises(ex.PoemTitleIsTooLongException):
        poem_vo.PoemTitle(poem_title_is_too_long * 200)

    with pytest.raises(ex.PoemTitleInCorrectFormatException):
        poem_vo.PoemTitle(poem_title_is_incorrect_format)


def test_poem_text_is_valid():
    poem_text_empty = ""

    with pytest.raises(ex.PoemTextIsEmptyException):
        poem_vo.PoemText(poem_text_empty)


def test_poem_date_is_valid():
    poem_date_empty = ""
    poem_date_is_too_long = "32.01.2020"
    poem_date_is_incorrect_format = "32.01.2020"

    with pytest.raises(ex.PoemDateIsEmptyException):
        poem_vo.PoemDate(poem_date_empty)

    with pytest.raises(ex.PoemDateIsTooLongException):
        poem_vo.PoemDate(poem_date_is_too_long * 200)

    with pytest.raises(ex.PoemDateInCorrectFormatException):
        poem_vo.PoemDate(poem_date_is_incorrect_format)


def test_poem_author_is_valid():
    poem_author_empty = ""
    poem_author_is_too_long = "Pushkin"
    poem_author_is_incorrect_format = "~_!Pushkin"

    with pytest.raises(ex.PoemAuthorIsEmptyException):
        poem_vo.PoemAuthor(poem_author_empty)

    with pytest.raises(ex.PoemAuthorIsTooLongException):
        poem_vo.PoemAuthor(poem_author_is_too_long * 200)

    with pytest.raises(ex.PoemAuthorInCorrectFormatException):
        poem_vo.PoemAuthor(poem_author_is_incorrect_format)


def test_poem_entity_is_valid():
    poem_title = poem_vo.PoemTitle("Onegin")
    poem_author = poem_vo.PoemAuthor("Pushkin")
    poem_text = poem_vo.PoemText("Onegin is Great Work")
    poem_date = poem_vo.PoemDate("06.06.2000")

    poem = Poem.create_poem(
        poem_title=poem_title,
        poem_author=poem_author,
        poem_text=poem_text,
        poem_date=poem_date,
    )

    assert poem.poem_title == poem_title
    assert poem.poem_author == poem_author
    assert poem.poem_text == poem_text
    assert poem.poem_date == poem_date
