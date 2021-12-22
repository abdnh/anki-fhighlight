import sys
import os
import re
import html

from anki import hooks

from anki.template import TemplateRenderContext

# FIXME: how to avoid conflicts with other add-ons that also inject the same modules?
addon_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(addon_dir, "vendor"))


from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers, guess_lexer
from pygments.formatters import HtmlFormatter


formatter = HtmlFormatter(noclasses=True, linenos=True)

cloze_re = re.compile("<span class=cloze>(.*)</span>")
html_re = re.compile("(<.*?>)")


def preprocess_field_text(field_text: str) -> str:
    field_text = html_re.sub("", field_text)
    field_text = html.unescape(field_text)
    field_text = cloze_re.sub(r"\1", field_text)
    field_text = field_text.replace("<br>", "\n")
    field_text = field_text.replace("&nbsp;", " ")
    return field_text


def highlight_text(context: TemplateRenderContext, field_text: str, options):
    config = {}
    for opt in map(lambda p: p.split("="), options):
        config[opt[0]] = opt[1]

    if lang := config.get("lang", None):
        if lang.startswith("#"):
            # treat as field reference
            try:
                lang = context.note()[lang[1:]].strip()
                lexer = get_lexer_by_name(lang, stripall=True)
            except Exception:
                lexer = guess_lexer(field_text, stripall=True)
        else:
            lexer = get_lexer_by_name(lang, stripall=True)
    else:
        lexer = guess_lexer(field_text, stripall=True)
    field_text = preprocess_field_text(field_text)

    highlighted = "<center>" + highlight(field_text, lexer, formatter) + "</center><br>"

    return highlighted


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
            filtered = highlight_text(context, field_text, filter_name.split()[1:])

    return filtered


hooks.field_filter.append(highlight_filter)
