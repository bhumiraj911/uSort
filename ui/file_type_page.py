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


class FileTypePage(QWidget):

    back_requested = Signal()

    category_selected = Signal()

    extension_selected = Signal()

    category_extension_selected = Signal()

    custom_selected = Signal()

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

        self.title_label = QLabel("File Type")

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

        self.subtitle_label = QLabel("Choose how you want to organize your files")

        self.subtitle_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 14px;
        """)

        self.layout.addWidget(self.subtitle_label)

        # Organization methods

        self.grid = QGridLayout()

        self.grid.setSpacing(theme.CARD_SPACING)

        self.category_card = OptionCard(
            "📁",
            "By Category",
            "Images / Documents / Videos",
        )

        self.extension_card = OptionCard(
            "📄",
            "By Extension",
            "JPG / PNG / PDF / MP4",
        )

        self.category_extension_card = OptionCard(
            "📁",
            "Category + Extension",
            "Images → JPG / PNG",
        )

        self.custom_card = OptionCard(
            "⚙️",
            "Custom",
            "Create your own groups",
        )

        self.grid.addWidget(
            self.category_card,
            0,
            0,
        )

        self.grid.addWidget(
            self.extension_card,
            0,
            1,
        )

        self.grid.addWidget(
            self.category_extension_card,
            1,
            0,
        )

        self.grid.addWidget(
            self.custom_card,
            1,
            1,
        )

        self.layout.addLayout(self.grid)

        self.layout.addStretch()

        # Connections

        self.category_card.clicked.connect(self.category_selected.emit)

        self.extension_card.clicked.connect(self.extension_selected.emit)

        self.category_extension_card.clicked.connect(
            self.category_extension_selected.emit
        )

        self.custom_card.clicked.connect(self.custom_selected.emit)
