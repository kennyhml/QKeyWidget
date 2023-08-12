from PySide6.QtWidgets import QVBoxLayout, QWidget, QTextEdit

from qkeywidget import QKeyWidget
import qkeywidget


class KeybindSettingWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        key_widget = QKeyWidget()
        key_widget.setToolTip("Manually created")

        regular_widget = QTextEdit()
        regular_widget.setToolTip("Wrapped")

        layout.addWidget(key_widget)
        layout.addWidget(regular_widget)
        self.setLayout(layout)
        qkeywidget.widget.wrap(regular_widget)


