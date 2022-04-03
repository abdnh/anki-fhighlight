from typing import Dict
from unittest import TestCase
import unittest

from src.fhighlight import (
    highlight_field,
    highlight_blocks,
    highlight_filter,
    preprocess_field_text,
)


class MockTemplateRenderContext:
    def __init__(self, fields: Dict[str, str]):
        self.fields = fields

    def note(self) -> Dict[str, str]:
        return self.fields


class TestHighlightFilter(TestCase):
    def setUp(self) -> None:
        self.context = MockTemplateRenderContext(
            {"Front": "", "Back": "", "Language": "python"}
        )

    def test_filter(self) -> None:
        text = 'print("hello")'
        highlighted1 = highlight_filter(text, "", "highlight lang=python", self.context)
        highlighted2 = highlight_field(self.context, text, {"lang": "python"})
        self.assertNotEqual(text, highlighted1)
        self.assertEqual(highlighted1, highlighted2)

    def test_filter_with_no_lang(self) -> None:
        text = 'print("hello")'
        highlighted = highlight_filter(text, "", "highlight", self.context)
        self.assertNotEqual(text, highlighted)

    def test_filter_with_invalid_lang(self) -> None:
        text = 'print("hello")'
        highlighted = highlight_filter(
            text, "", "highlight lang=zxzxzxzxzx", self.context
        )
        self.assertNotEqual(text, highlighted)

    def test_filter_with_lang_field(self) -> None:
        text = 'print("hello")'
        highlighted1 = highlight_filter(
            text, "", "highlight lang=#Language", self.context
        )
        highlighted2 = highlight_field(self.context, text, {"lang": "#Language"})
        self.assertNotEqual(text, highlighted1)
        self.assertEqual(highlighted1, highlighted2)

    def test_filter_with_invalid_lang_field_name(self) -> None:
        text = 'print("hello")'
        with self.assertRaises(Exception):
            highlight_filter(text, "", "highlight lang=#foo", self.context)

    def test_filter_with_empty_lang_field(self) -> None:
        self.context.fields["Language"] = ""
        text = 'print("hello")'
        highlighted1 = highlight_filter(
            text, "", "highlight lang=#Language", self.context
        )
        highlighted2 = highlight_field(self.context, text, {"lang": "#Language"})
        self.assertNotEqual(text, highlighted1)
        self.assertEqual(highlighted1, highlighted2)

    def test_filter_with_invalid_lang_field(self) -> None:
        self.context.fields["Language"] = "zxzxzxzxzx"
        text = 'print("hello")'
        highlighted1 = highlight_filter(
            text, "", "highlight lang=#Language", self.context
        )
        highlighted2 = highlight_field(self.context, text, {"lang": "#Language"})
        self.assertNotEqual(text, highlighted1)
        self.assertEqual(highlighted1, highlighted2)

    def test_highlight_blocks(self) -> None:
        text = """
            #highlight:python
            print("hello world!")
            #highlight
        """
        highlighted = highlight_blocks(text)
        self.assertNotEqual(text, highlighted)

    def test_highlight_blocks_with_invalid_lang(self) -> None:
        text = """
            #highlight:zxzxzxzxzx
            print("hello world!")
            #highlight
        """
        highlighted = highlight_blocks(text)
        # An invalid language name result in the add-on guessing the text language using guess_lexer()
        self.assertNotEqual(text, highlighted)

    def test_highlight_blocks_with_empty_lang(self) -> None:
        text = """
            #highlight:
            print("hello world!")
            #highlight
        """
        highlighted = highlight_blocks(text)
        # Not specifying a language name will result in no highlighting
        self.assertEqual(text, highlighted)

    def test_text_cleaning(self) -> None:
        text = """<br><div>print("hello world!")</div>"""
        cleaned = preprocess_field_text(text)
        expected = """\nprint("hello world!")\n"""
        self.assertEqual(cleaned, expected)


if __name__ == "__main__":
    unittest.main()
