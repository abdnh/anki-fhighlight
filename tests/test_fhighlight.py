from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, cast

import pytest

if TYPE_CHECKING:
    from anki.notes import Note

from src.fhighlight import (
    FhighlightException,
    highlight_blocks,
    highlight_field,
    highlight_filter,
    preprocess_field_text,
)


@dataclass
class MockNote:
    fields: Dict[str, str]

    def __getitem__(self, name: str) -> str:
        return self.fields[name]

    def __setitem__(self, name: str, value: str) -> None:
        self.fields[name] = value


@pytest.fixture
def note() -> "Note":
    return cast(
        "Note",
        MockNote({"Front": "", "Back": "", "Language": "python"}),
    )


def test_basic_filter(note: "Note") -> None:
    text = 'print("hello")'
    highlighted1 = highlight_filter(note, text, "", "highlight lang=python")
    highlighted2 = highlight_field(note, text, {"lang": "python"})
    assert text != highlighted1
    assert highlighted1 == highlighted2


def test_filter_with_no_lang(note: "Note") -> None:
    text = 'print("hello")'
    highlighted = highlight_filter(note, text, "", "highlight")
    assert text != highlighted


def test_filter_with_invalid_lang(note: "Note") -> None:
    text = 'print("hello")'
    highlighted = highlight_filter(note, text, "", "highlight lang=zxzxzxzxzx")
    assert text != highlighted


def test_filter_with_lang_field(note: "Note") -> None:
    text = 'print("hello")'
    highlighted1 = highlight_filter(
        note,
        text,
        "",
        "highlight lang=#Language",
    )
    highlighted2 = highlight_field(note, text, {"lang": "#Language"})
    assert text != highlighted1
    assert highlighted1 == highlighted2


def test_filter_with_invalid_lang_field_name(
    note: "Note",
) -> None:
    text = 'print("hello")'
    with pytest.raises(FhighlightException):
        highlight_filter(note, text, "", "highlight lang=#foo")


def test_filter_with_empty_lang_field(note: "Note") -> None:
    note["Language"] = ""
    text = 'print("hello")'
    highlighted1 = highlight_filter(note, text, "", "highlight lang=#Language")
    highlighted2 = highlight_field(note, text, {"lang": "#Language"})
    assert text != highlighted1
    assert highlighted1 == highlighted2


def test_filter_with_invalid_lang_field(note: "Note") -> None:
    note["Language"] = "zxzxzxzxzx"
    text = 'print("hello")'
    highlighted1 = highlight_filter(
        note,
        text,
        "",
        "highlight lang=#Language",
    )
    highlighted2 = highlight_field(note, text, {"lang": "#Language"})
    assert text != highlighted1
    assert highlighted1 == highlighted2


def test_highlight_blocks() -> None:
    text = """
        ```python
        print("hello world!")
        ```
    """
    highlighted = highlight_blocks(text)
    assert text != highlighted


def test_highlight_blocks_with_invalid_lang() -> None:
    text = """
        ```zxzxzxzxzx
        print("hello world!")
        ```
    """
    highlighted = highlight_blocks(text)
    # An invalid language name results in the add-on guessing the text language using guess_lexer()
    assert text != highlighted


def test_highlight_blocks_with_empty_lang() -> None:
    text = """
        ```
        print("hello world!")
        ```
    """
    highlighted = highlight_blocks(text)
    # Not specifying a language name will result in no highlighting
    assert text == highlighted


def test_text_cleaning() -> None:
    text = """<br><div>print("hello world!")</div>"""
    cleaned = preprocess_field_text(text)
    expected = """\nprint("hello world!")\n"""
    assert cleaned == expected
