import html
import re
import sys
from typing import TYPE_CHECKING, Dict, Iterator, Match, Sequence, Tuple

if TYPE_CHECKING:
    from anki.notes import Note

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexer import Lexer
from pygments.lexers import get_all_lexers, get_lexer_by_name, guess_lexer

if "pytest" not in sys.modules:
    from .config import config

    formatter_options = config["formatter_options"]
else:
    formatter_options = {}
formatter = HtmlFormatter(noclasses=True, **formatter_options)

cloze_re = re.compile("<span class=cloze>(.*)</span>")
html_re = re.compile("(<.*?>)")


class FhighlightException(Exception):
    pass


def preprocess_field_text(field_text: str) -> str:
    field_text = field_text.replace("<br>", "\n")
    field_text = field_text.replace("</div>", "\n")
    field_text = html_re.sub("", field_text)
    field_text = html.unescape(field_text)
    field_text = cloze_re.sub(r"\1", field_text)
    field_text = field_text.replace("&nbsp;", " ")
    return field_text


def highlight_text(text: str, lexer: Lexer) -> str:
    return highlight(text, lexer, formatter)


def fhighlight_get_lexer(lang: str, text: str) -> Lexer:
    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except:
        lexer = guess_lexer(text, stripall=True)
    return lexer


def highlight_field(note: "Note", field_text: str, options: Dict[str, str]) -> str:
    field_text = preprocess_field_text(field_text)
    if lang := options.get("lang", None):
        if lang.startswith("#"):
            # treat as field reference
            try:
                field = lang[1:]
                lang = note[field].strip()
            except KeyError as exc:
                raise FhighlightException(
                    f"Field '{field}' used in the highlight filter does not exist"
                ) from exc
        lexer = fhighlight_get_lexer(lang, field_text)
    else:
        lexer = guess_lexer(field_text, stripall=True)

    return highlight_text(field_text, lexer)


def highlight_filter(
    note: "Note",
    field_text: str,
    field_name: str,
    filter_name: str,
) -> str:
    filtered = field_text
    if filter_name.startswith("highlight"):
        if filter_name.startswith("highlight-list-lexers"):
            filtered = "<br>".join(
                map(lambda l: f"name: {l[0]}, aliases = {l[1]}", get_all_lexers())
            )
        else:
            options = {}
            for opt in map(lambda p: p.split("="), filter_name.split()[1:]):
                options[opt[0]] = opt[1]
            filtered = highlight_field(note, filtered, options)

    return filtered


highlight_in_field_re = re.compile(r"```([^<\s]*)(.*?)```", re.DOTALL)


def highlight_blocks(text: str) -> str:
    """
    Process code blocks in fields delimited by triple backticks.
    """

    def highligh_block(m: Match) -> str:
        lang = m.group(1)
        text = m.group(2)
        text = preprocess_field_text(text)
        lexer = fhighlight_get_lexer(lang, text)
        return highlight_text(text, lexer)

    return highlight_in_field_re.sub(highligh_block, text)


def fhighlight_get_all_lexers() -> (
    Iterator[Tuple[str, Sequence[str], Sequence[str], Sequence[str]]]
):
    return get_all_lexers()
