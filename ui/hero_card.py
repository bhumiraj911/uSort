from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from ui import theme


class HeroCard(QFrame):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(175)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.CARD};
                border: 1px solid {theme.BORDER};
                border-radius: {theme.CARD_RADIUS}px;
            }}

            QLabel {{
                background: transparent;
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
            }}

            QPushButton:hover {{
                background-color: #4F93FF;
            }}
        """)

        layout = QVBoxLayout(self)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        title = QLabel("Drop a folder here or browse")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        browse = QPushButton("Select Folder")
        browse.setFixedSize(180,46)
        
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(browse, alignment=Qt.AlignmentFlag.AlignCenter)
        