from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QTextBlockFormat, QMouseEvent
from PySide6.QtWidgets import QTextEdit, QWidget

from . import tools

_MODIFIERS = {"Shift", "Alt", "Ctrl"}


class QKeyWidget(QTextEdit):
    """Wrapper for a `QTextEdit` to make it's primary purpose to capture
    and display key combinations.

    Parameters:
    ----------
    parent :class:`Optional[QWidget]`:
        The parent widget of the `QKeyWidget`

    modifiersAllowed :class:`bool`:
        Whether modifiers such as `"Alt"`, `"Shift"` and `"Ctrl"` are allowed.

    maxCombinationLength :class:`in`:
        The maximum length of the combination. Example `3`: `"Shift" + "Ctrl" + "A"`
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        modifiersAllowed: bool = True,
        maxCombinationLength: int = 3,
    ):
        super().__init__(parent)
        self._modifiersAllowed = modifiersAllowed
        self._maxCombinationLength = maxCombinationLength
        self.setCursorWidth(0)
        self.displayCombination("")

    @property
    def modifiersAllowed(self) -> bool:
        return self._modifiersAllowed

    @modifiersAllowed.setter
    def modifiersAllowed(self, allowed: bool) -> None:
        # if modifiers are now forbidden, our current combination may be invalid.
        if not allowed and any(mod in self.combination for mod in _MODIFIERS):
            self.displayCombination("")

        self._modifiersAllowed = allowed

    @property
    def maxCombinationLength(self) -> int:
        return self._maxCombinationLength

    @maxCombinationLength.setter
    def maxCombinationLength(self, length: int) -> None:
        # current length could now be too large, so the combination may be invalid.
        if self.currentCombinationLength > length:
            self.displayCombination("")

        self._maxCombinationLength = length

    @property
    def currentCombinationLength(self) -> int:
        if not self.combination:
            return 0
        return len(self.combination.split(" + "))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Captures the pressed sequence of keys and displays it in the widget.

        Modifiers will only be taken into consideration if allowed.
        """
        key = Qt.Key(event.key())
        keyName = key.name.split("_")[1]
        if keyName == "Return":
            return self.clearFocus()

        # parses the captured event as it comes in mainly hard to display data
        mods = tools.extractModifiers(event.modifiers())
        self.combination = tools.stringifyCombination(mods, keyName)
        self.displayCombination()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handles the `QMouseEvent` on the widget in order to allow using mouse4
        and mouse5 as keybinds. Modifiers together with it are not suported."""
        button = event.button()
        key = None
        if button.name == "ForwardButton":
            key = "mouse5"
        elif button.name == "BackButton":
            key = "mouse4"

        self.displayCombination(key)

    def displayCombination(self, text: Optional[str] = None) -> None:
        """Displays the combination"""
        if text is not None:
            self.combination = text

        self.setText(self.combination)

        # align the text to the center of the `QTextEdit`
        cursor = self.textCursor()
        blockFormat = QTextBlockFormat()
        blockFormat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cursor.setBlockFormat(blockFormat)
        self.setTextCursor(cursor)


def wrap(widget: QTextEdit, *, modifiersAllowed=True, maxCombinationLength=3):
    """Wraps an existing `QTextEdit` to give it the `QKeyWidget` functionality.

    This is done by creating bound methods to the instance using the methods of the
    `QKeyWidget` class.

    In simpler terms, this will override methods of the original `QTextEdit` widget and add variables
    from the custom implementation of the `QKeyWidget`, while still retaining the context of the widget
    instance.
    """
    widget.setCursorWidth(0)
    widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # compensate for the fact that we cant truly initialize the QKeyWidget
    setattr(widget, "_modifiersAllowed", modifiersAllowed)
    setattr(widget, "_maxCombinationLength", maxCombinationLength)
    setattr(widget, "combination", widget.toPlainText())

    # __get__ creates a bound method to the widget instance for the function.
    for name, func in QKeyWidget.__dict__.items():
        if callable(func) or isinstance(func, property):
            bound_function = func.__get__(widget, QTextEdit)
            widget.__setattr__(name, bound_function)

    widget.displayCombination()  # type: ignore[attr-defined]
