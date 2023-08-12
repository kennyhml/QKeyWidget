from PySide6.QtCore import Qt


def extractModifiers(modifiers: Qt.KeyboardModifier) -> list[str]:
    """Extracts the alt, shift and ctrl modifiers from a `KeyboardModifier` by using a bitmask.

    Returns them as an array of strings with the first letter capitalized.
    """
    ret = []

    if modifiers & Qt.KeyboardModifier.AltModifier:
        ret.append("Alt")
    if modifiers & Qt.KeyboardModifier.ShiftModifier:
        ret.append("Shift")
    if modifiers & Qt.KeyboardModifier.ControlModifier:
        ret.append("Ctrl")

    return ret


def stringifyCombination(modifiers: list[str], key: str) -> str:
    """Stringifies a combination of modifiers and the pressed key.

    Examples:
    ```py
    stringify_combination(["Alt", "Shift"], "A")
    >>> "Alt + Shift + A"

    stringify_combination([], "B")
    >>> "B"

    stringify_combination(["Shift"], "Shift")
    >>> "Shift"
    """

    key = toSymbol(key)
    for i in range(len(modifiers)):
        modifiers[i] = toSymbol(modifiers[i])

    if key in modifiers:
        modifiers.remove(key)

    combination = ""
    if modifiers:
        mods = (" + ".join(modifiers) if len(modifiers) > 1 else f"{modifiers[0]}" )+ ' + '
        combination += mods

    combination += key

    return combination


def toSymbol(text: str) -> str:
    return _SYMBOL_MAP.get(text, text)


_SYMBOL_MAP = {
    "Comma": ",",
    "Question": "?",
    "Period": ".",
    "Slash": "/",
    "Semicolon": ";",
    "Colon": ":",
    "Less": "<",
    "Greater": ">",
    "Minus": "-",
    "Equal": "=",
    "Plus": "+",
    "Underscore": "_",
}
