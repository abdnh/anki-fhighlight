import sys


def on_card_will_show(text: str, card: "Card", kind: str) -> str:
    return highlight_blocks(text)


if "unittest" not in sys.modules:
    from anki import hooks
    from anki.cards import Card
    from aqt import gui_hooks
    from aqt.utils import showWarning
    from anki.template import TemplateRenderContext

    from .fhighlight import highlight_filter, highlight_blocks

    def on_highligth_filter(
        field_text: str,
        field_name: str,
        filter_name: str,
        context: TemplateRenderContext,
    ) -> str:
        try:
            return highlight_filter(field_text, field_name, filter_name, context)
        except Exception as e:
            showWarning(str(e), title="FHighlight Add-on")
            return field_text

    hooks.field_filter.append(on_highligth_filter)
    gui_hooks.card_will_show.append(on_card_will_show)
