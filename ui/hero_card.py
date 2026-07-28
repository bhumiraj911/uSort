from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from ui import theme


class HeroCard(QFrame):
    folder_dropped = Signal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("heroCard")
        self.setFixedHeight(175)
        self.setAcceptDrops(True)

        self.setStyleSheet(f"""
            QFrame#heroCard {{
                background-color: {theme.CARD};
                border: 1px solid {theme.BORDER};
                border-radius: {theme.CARD_RADIUS}px;
            }}

            QLabel {{
                background: transparent;
                border: none;
                color: {theme.TEXT};
                font-size: 22px;
                font-weight: 500;
            }}

            QPushButton {{
                background-color: {theme.PRIMARY};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }}

            QPushButton:hover {{
                background-color: #4F93FF;
            }}

            QPushButton:pressed {{
                background-color: #2F6FD6;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("Drop a folder here or browse")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.browse_button = QPushButton("Select Folder")
        self.browse_button.setFixedSize(180, 46)

        layout.addWidget(self.title)
        layout.addWidget(
            self.browse_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        print("drop Event")
        
        urls = event.mimeData().urls()

        if not urls:
            return

        folder = urls[0].toLocalFile()
        
        print(f"Dropped Folder: {folder}")
        

        self.folder_dropped.emit(folder)

        event.acceptProposedAction()