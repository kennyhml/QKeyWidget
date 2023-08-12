from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QTextBlockFormat
from PySide6.QtWidgets import QTextEdit, QWidget

from . import tools


class QKeyWidget(QTextEdit):
    """Wrapper for a `QTextEdit` to make it's primary purpose to capture
    and display key combinations."""

    def __init__(self, text=None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setCursorWidth(0)
        self.combination = "-"
        self.displayCombination()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Captures the pressed sequence of keys and displays it in the widget."""
        key = Qt.Key(event.key())
        keyName = key.name.split("_")[1]

        # parses the captured event as it comes in mainly hard to display data
        mods = tools.extractModifiers(event.modifiers())
        self.combination = tools.stringifyCombination(mods, keyName)
        self.displayCombination()

    def displayCombination(self) -> None:
        """Displays the combination"""
        self.setText(self.combination)

        # align the text to the center of the `QTextEdit`
        cursor = self.textCursor()
        blockFormat = QTextBlockFormat()
        blockFormat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cursor.setBlockFormat(blockFormat)
        self.setTextCursor(cursor)


def wrap(widget: QTextEdit) -> None:
    """Wraps an existing `QTextEdit` to give it the `QKeyWidget` functionality.
    
    This is done by creating bound methods to the instance using the methods of the 
    `QKeyWidget` class.

    In simpler terms, this will override the `keyPressEvent` method of the original `QTextEdit` widget 
    with the custom implementation of the `QKeyWidget`, while still retaining the context of the widget 
    instance.
    """
    widget.setCursorWidth(0)
    widget.displayCombination = QKeyWidget.displayCombination.__get__(widget, QTextEdit)  # type: ignore
    widget.keyPressEvent = QKeyWidget.keyPressEvent.__get__(widget, QTextEdit)  # type: ignore
    widget.combination = "-" # type: ignore
    widget.displayCombination()  # type: ignore
