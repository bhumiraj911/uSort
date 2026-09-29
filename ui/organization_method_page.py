from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
)

from ui import theme
from ui.option_card import OptionCard


class OrganizationMethodPage(QWidget):

    back_requested = Signal()

    file_type_selected = Signal()

    date_selected = Signal()

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            theme.PADDING,
            theme.PADDING,
            theme.PADDING,
            theme.PADDING,
        )

        self.layout.setSpacing(theme.CARD_SPACING)

        # Top bar

        top_bar = QHBoxLayout()

        self.back_button = QPushButton("← Back")

        self.back_button.setCursor(Qt.PointingHandCursor)

        self.back_button.clicked.connect(self.back_requested.emit)

        self.title_label = QLabel("Organization Method")

        self.title_label.setStyleSheet(f"""
            color: {theme.TEXT};
            font-size: 24px;
            font-weight: 600;
        """)

        top_bar.addWidget(self.back_button)

        top_bar.addSpacing(20)

        top_bar.addWidget(self.title_label)

        top_bar.addStretch()

        self.layout.addLayout(top_bar)

        # Subtitle

        self.subtitle_label = QLabel(
            "Choose how you want to organize the selected files"
        )

        self.subtitle_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 14px;
        """)

        self.layout.addWidget(self.subtitle_label)

        # Method cards

        self.grid = QGridLayout()

        self.grid.setSpacing(theme.CARD_SPACING)

        self.file_type_card = OptionCard(
            "📂",
            "File Type",
            "Organize files by their type",
        )

        self.date_card = OptionCard(
            "📅",
            "Date",
            "Organize files by date",
        )

        self.grid.addWidget(
            self.file_type_card,
            0,
            0,
        )

        self.grid.addWidget(
            self.date_card,
            0,
            1,
        )

        self.layout.addLayout(self.grid)

        self.layout.addStretch()

        # Connections

        self.file_type_card.clicked.connect(self.file_type_selected.emit)

        self.date_card.clicked.connect(self.date_selected.emit)
