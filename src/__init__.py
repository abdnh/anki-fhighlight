import sys
import os
import re
import html
from typing import List, Match

from anki import hooks
from anki.cards import Card
from aqt import gui_hooks

from anki.template import TemplateRenderContext

# FIXME: how to avoid conflicts with other add-ons that also inject the same modules?
addon_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(addon_dir, "vendor"))

from pygments.lexer import Lexer
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers, guess_lexer
from pygments.formatters import HtmlFormatter


formatter = HtmlFormatter(noclasses=True, linenos=True)

cloze_re = re.compile("<span class=cloze>(.*)</span>")
html_re = re.compile("(<.*?>)")


def preprocess_field_text(field_text: str) -> str:
    field_text = field_text.replace("<br>", "\n")
    field_text = html_re.sub("", field_text)
    field_text = html.unescape(field_text)
    field_text = cloze_re.sub(r"\1", field_text)
    field_text = field_text.replace("&nbsp;", " ")
    return field_text


def highlight_text(text, lexer: Lexer) -> str:
    return "<center>" + highlight(text, lexer, formatter) + "</center><br>"


def fhighlight_get_lexer(lang: str, text: str) -> Lexer:
    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except:
        lexer = guess_lexer(text, stripall=True)
    return lexer


def highlight_field(
    context: TemplateRenderContext, field_text: str, options: List[str]
) -> str:
    config = {}
    for opt in map(lambda p: p.split("="), options):
        config[opt[0]] = opt[1]
    field_text = preprocess_field_text(field_text)
    if lang := config.get("lang", None):
        if lang.startswith("#"):
            # treat as field reference
            lang = context.note()[lang[1:]].strip()
        lexer = fhighlight_get_lexer(lang, field_text)
    else:
        lexer = guess_lexer(field_text, stripall=True)

    return highlight_text(field_text, lexer)


def highlight_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    context: TemplateRenderContext,
) -> str:

    filtered = field_text
    if filter_name.startswith("highlight"):
        if filter_name.startswith("highlight-list-lexers"):
            filtered = "<br>".join(
                map(lambda l: f"name: {l[0]}, aliases = {l[1]}", get_all_lexers())
            )
        else:
            filtered = highlight_field(context, filtered, filter_name.split()[1:])

    return filtered


highlight_in_field_re = re.compile("#highlight:([^<\s]+)(.*?)#highlight", re.DOTALL)


def highlight_blocks(text: str):
    """
    Process code blocks in fields delimited by `#highlight`. E.g:
    ```
      #highlight:python
      print("hello world!")
      #highlight
    ```
    """

    def highligh_block(m: Match):
        lang = m.group(1)
        text = m.group(2)
        text = preprocess_field_text(text)
        lexer = fhighlight_get_lexer(lang, text)
        return highlight_text(text, lexer)

    return highlight_in_field_re.sub(highligh_block, text)


def on_card_will_show(text: str, card: Card, kind: str) -> str:
    return highlight_blocks(text)


hooks.field_filter.append(highlight_filter)
gui_hooks.card_will_show.append(on_card_will_show)
