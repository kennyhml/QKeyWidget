from PySide6.QtWidgets import QApplication
import layout  # type: ignore

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = layout.KeybindSettingWindow()
    window.show()

    sys.exit(app.exec_())
