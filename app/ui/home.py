from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap

class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CTF Knowledge Base")
        self.resize(700, 600)

        layout = QVBoxLayout()

        assets_path = Path(__file__).resolve().parent.parent / "assets"
        avatar_label = QLabel()
        pixmap = QPixmap(str(assets_path / "avatar.png"))
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        avatar_label.setPixmap(pixmap)
        avatar_label.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome back!")
        title.setAlignment(Qt.AlignCenter)

        btn1 = QPushButton("Techniques")
        btn2 = QPushButton("TryHackMe")
        btn3 = QPushButton("Exit")
        btn2.setToolTip("An overview of all the TryHackMe challenges")

        btn3.clicked.connect(self.close)

        layout.addWidget(avatar_label)
        layout.addWidget(title)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        self.setLayout(layout)