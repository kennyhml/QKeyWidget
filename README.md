# QKeyWidget
QKeyWidget provides a wrapper for PySide's `QTextEdit` (created as a wrapped instance or wrapped around an existing instance).

This wrapper aims to turn the widget into one that is useful to set key combinations by simply focusing the widget and entering pressing the combination.

## An example of how that might look:

<img src="https://cdn.discordapp.com/attachments/662412610565570583/1139978526372667522/qkeywidget_showcase.gif" width="300" height="100" />

## Features:
- Limit `QKeyWidget` to keys only, no modifiers allowed (alt, shift, ctrl)
- Limit the maximum combination length of the `QKeyWidget`
- Supports mouse4 and mouse5 (mouse side - back and forward buttons)
- Gracefully aligns the entered key combination centered
- Conform with the PySide style
- No PySide monkey patching
- Fully typed
  
## How to use?
The usage is very simple and minimalistic, you can either create a `QKeyWidget` instead of a `QTextEdit` (which is just a thin wrapper) or, if you already have
an existing `QTextEdit` which you would like to give the `QKeyWidget` functionality, you can use the `wrap` function.

To create a fresh widget, it's really the same as creating the `QTextEdit`:
```py
from qkeywidget import QKeyWidget

keyWidget = QKeyWidget()
```
And if you already have an existing `QTextEdit`:
```py
import qkeywidget

regularTextEdit = QTextEdit()
qkeywidget.wrap(regularTextEdit)
```
`regularTextEdit` has now magically been modified to support all the operations that `QKeyWidget` does!
