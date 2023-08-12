from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QTextBlockFormat
from PySide6.QtWidgets import QTextEdit, QWidget

from . import tools


class QKeyWidget(QTextEdit):
    def __init__(self, text=None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setCursorWidth(0)
        self.setText("-")

    def keyPressEvent(self, event: QKeyEvent):
        self.setText("")
        key = Qt.Key(event.key())
        key_name = key.name.split("_")[1]

        mods = tools.extract_modifiers(event.modifiers())
        if key_name in mods:
            mods.remove(key_name)

        combination = ""
        if mods:
            combination += " + ".join(mods) if len(mods) > 1 else f"{mods[0]} + "

        combination += key_name
        self.setText(combination)

    def setText(self, text: str) -> None:
        super().setText(text)
        cursor = self.textCursor()
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cursor.setBlockFormat(block_format)
        self.setTextCursor(cursor)
