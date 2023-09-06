import os
from typing import TYPE_CHECKING, List

from anki import hooks

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.template import TemplateRenderContext

from aqt import gui_hooks
from aqt.editor import Editor
from aqt.qt import *
from aqt.utils import showWarning

from .config import config
from .consts import consts
from .fhighlight import fhighlight_get_all_lexers, highlight_blocks, highlight_filter


def on_card_will_show(text: str, card: "Card", kind: str) -> str:
    return highlight_blocks(text)


def on_highlight_filter(
    field_text: str,
    field_name: str,
    filter_name: str,
    context: "TemplateRenderContext",
) -> str:
    try:
        return highlight_filter(context.note(), field_text, field_name, filter_name)
    except Exception as e:
        showWarning(str(e), title=consts.name)
        return field_text


def add_editor_button(buttons: List[str], editor: Editor) -> None:
    def on_button(editor: Editor) -> None:
        dialog = QDialog(editor.widget)
        dialog.setWindowTitle(consts.name)
        label = QLabel("Language:")
        combo = QComboBox(dialog)
        def_lang = config.get("def_lang", "python")
        def_lang_idx = 0
        for i, ent in enumerate(fhighlight_get_all_lexers()):
            if ent[0].lower() == def_lang.lower():
                def_lang_idx = i
            combo.addItem(ent[0], ent[1][0] if len(ent[1]) > 0 else ent[0])
        combo.setCurrentIndex(def_lang_idx)
        ok_button = QPushButton()
        ok_button.setText("OK")
        ok_button.setDefault(True)
        ok_button.setAutoDefault(True)

        def accept() -> None:
            lang = combo.currentText()
            lang_alias = combo.currentData()
            dialog.close()
            editor.web.eval(
                f"setTimeout(() => wrap('```{lang_alias}<br>', '<br>```'), 10)"
            )
            config["def_lang"] = lang

        qconnect(ok_button.clicked, accept)
        cancel_button = QPushButton()
        cancel_button.setText("Cancel")
        # pylint: disable=unnecessary-lambda
        qconnect(cancel_button.clicked, lambda: dialog.reject())
        combo_hbox = QHBoxLayout()
        combo_hbox.addWidget(label)
        combo_hbox.addWidget(combo)
        buttons_box = QHBoxLayout()
        buttons_box.addWidget(cancel_button)
        buttons_box.addWidget(ok_button)
        layout = QVBoxLayout()
        layout.addLayout(combo_hbox)
        layout.addLayout(buttons_box)
        dialog.setLayout(layout)
        dialog.exec()

    button = editor.addButton(
        icon=os.path.join(consts.dir, "icon.svg"),
        cmd="fhighlight",
        func=on_button,
        tip=consts.name,
        keys=config.get("shortcut", "Alt+s"),
    )
    buttons.append(button)


def init_hooks() -> None:
    hooks.field_filter.append(on_highlight_filter)
    gui_hooks.card_will_show.append(on_card_will_show)
    gui_hooks.editor_did_init_buttons.append(add_editor_button)
