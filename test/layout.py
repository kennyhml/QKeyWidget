from PySide6.QtWidgets import QVBoxLayout, QWidget

from qkeywidget import QKeyWidget


class KeybindSettingWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        key_widget = QKeyWidget()
        layout.addWidget(key_widget)
        self.setLayout(layout)
