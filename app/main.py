import sys
from PySide6.QtWidgets import QApplication

from ui.home import Home


def main():
    app = QApplication(sys.argv)

    window = Home()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()