from pathlib import Path
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout,
                               QHBoxLayout, QListWidget, QTextBrowser, QMessageBox)
from PySide6.QtGui import QPixmap, QTextDocument
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


# --- Endgültig optimierter QTextBrowser für fehlerfreie Medien-Ressourcen ---
class NetworkTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nam = QNetworkAccessManager(self)
        self.nam.finished.connect(self.handle_network_reply)
        self.setOpenExternalLinks(True)

    def loadResource(self, type_int, qurl):
        # 1 = QTextDocument.HtmlResource (Bilder im Dokument)
        if type_int == 1:
            if qurl.scheme() in ["http", "https"]:
                cached = self.document().resource(1, qurl)
                if cached:
                    return cached

                # Bild asynchron von GitHub im Hintergrund ziehen
                req = QNetworkRequest(qurl)
                self.nam.get(req)

                # Liefert ein transparentes Dummy-Bild zurück (entfernt das Datei-Icon "￼")
                empty_pixmap = QPixmap(1, 1)
                empty_pixmap.fill(Qt.transparent)
                return empty_pixmap

        return super().loadResource(type_int, qurl)

    def handle_network_reply(self, reply):
        if reply.error() == QNetworkReply.NoError:
            url = reply.url()
            data = reply.readAll()

            pixmap = QPixmap()
            pixmap.loadFromData(data)

            # Bild im Dokumenten-Cache registrieren
            self.document().addResource(1, url, pixmap)

            # MAGISCHE ZEILE: Zwingt Qt, das HTML-Layout neu zu berechnen.
            # Dadurch verschwindet der Platzhalter und das echte Bild erscheint sofort!
            self.document().documentLayout().update()
            self.viewport().update()

        reply.deleteLater()


# --- Das Übersichtsfenster für deine flache TryHackMe-Struktur ---
class TryHackMeWindow(QWidget):
    def __init__(self, thm_folder_path):
        super().__init__()
        self.setWindowTitle("TryHackMe Writeups")
        self.resize(950, 650)
        self.thm_folder = Path(thm_folder_path)

        main_layout = QHBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(280)
        self.list_widget.itemSelectionChanged.connect(self.load_markdown_content)

        self.text_viewer = NetworkTextBrowser()

        # Suchpfad für lokale Bilder registrieren
        self.text_viewer.setSearchPaths([str(self.thm_folder)])

        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.text_viewer)
        self.setLayout(main_layout)

        self.populate_list()

    def populate_list(self):
        """Liest alle .md-Dateien direkt aus dem Ordner aus."""
        if not self.thm_folder.exists():
            QMessageBox.warning(self, "Fehler", f"Der TryHackMe-Ordner wurde nicht gefunden unter:\n{self.thm_folder}")
            return

        self.md_files = sorted(list(self.thm_folder.glob("*.md")))

        for file_path in self.md_files:
            self.list_widget.addItem(file_path.stem)

    def load_markdown_content(self):
        """Lädt das Writeup, wandelt es sauber in HTML um und setzt die Basis-URL."""
        selected_index = self.list_widget.currentRow()
        if selected_index >= 0:
            target_file = self.md_files[selected_index]
            try:
                content = target_file.read_text(encoding="utf-8")

                # Basis-URL auf deinen lokalen TryHackMe-Ordner setzen (für lokale .png/.jpg-Bilder)
                folder_url = QUrl.fromLocalFile(str(self.thm_folder) + "/")
                self.text_viewer.document().setBaseUrl(folder_url)

                # SCHRITT: Nutze ein temporäres Dokument, um Markdown fehlerfrei in HTML zu parsen
                converter_doc = QTextDocument()
                converter_doc.setMarkdown(content)
                html_content = converter_doc.toHtml()

                # CSS-Injektion: Verhindert, dass riesige Screenshots den Text-Viewer sprengen
                css_style = "<style>img { max-width: 100%; height: auto; display: block; margin: 10px 0; }</style>"
                html_content = html_content.replace("<head>", f"<head>{css_style}")

                # Übergabe des generierten HTML an den Viewer
                self.text_viewer.setHtml(html_content)

            except Exception as e:
                self.text_viewer.setText(f"Fehler beim Lesen der Datei:\n{e}")


# --- Dein Hauptfenster (Home) ---
class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CTF Knowledge Base")
        self.resize(700, 600)

        layout = QVBoxLayout()

        # --- DYNAMISCHE PFADSUCHE ---
        current_dir = Path(__file__).resolve().parent
        root_path = current_dir
        while root_path.name != "ctf-writeups" and root_path.parent != root_path:
            root_path = root_path.parent

        if root_path.name != "ctf-writeups":
            root_path = current_dir.parent

        self.thm_path = root_path / "TryHackMe"

        assets_path = root_path / "assets"
        if not assets_path.exists():
            assets_path = root_path / "app" / "assets"

        # --- AUDIO-LOGIK ---
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        sound_path = assets_path / 'cyber_click.wav'
        if sound_path.exists():
            self.player.setSource(QUrl.fromLocalFile(str(sound_path)))
            self.audio_output.setVolume(0.4)

        # --- AVATAR BILD-CHECK ---
        avatar_label = QLabel()
        avatar_file = assets_path / "avatar.png"

        if avatar_file.exists():
            pixmap = QPixmap(str(avatar_file))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                avatar_label.setPixmap(pixmap)

        avatar_label.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome back!")
        title.setAlignment(Qt.AlignCenter)

        btn1 = QPushButton("Techniques")
        btn2 = QPushButton("TryHackMe")
        btn3 = QPushButton("Exit")
        btn2.setToolTip("An overview of all the TryHackMe challenges")

        btn1.clicked.connect(self.play_click)
        btn2.clicked.connect(self.play_click)
        btn3.clicked.connect(self.play_click)

        btn2.clicked.connect(self.open_tryhackme)
        btn3.clicked.connect(self.close)

        layout.addWidget(avatar_label)
        layout.addWidget(title)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        self.setLayout(layout)

    def play_click(self):
        self.player.stop()
        self.player.play()

    def open_tryhackme(self):
        """Öffnet die TryHackMe-Übersicht."""
        self.thm_window = TryHackMeWindow(self.thm_path)
        self.thm_window.show()