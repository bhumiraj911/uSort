from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from ui import theme

class OptionCard(QFrame):
    clicked = Signal()

    def __init__(self, icon: str, title: str, description: str):
        super().__init__()

        self.setObjectName("optionCard")
        self.selected = False

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(260, 170)

        # Icon
        self.icon_label = QLabel(icon)
        self.icon_label.setAlignment(Qt.AlignLeft)
        self.icon_label.setStyleSheet("""
            font-size: 28px;
        """)

        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            color: {theme.TEXT};
            font-size: 16px;
            font-weight: 600;
        """)

        # Description
        self.description_label = QLabel(description)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 12px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            theme.PADDING,
            theme.PADDING,
            theme.PADDING,
            theme.PADDING
        )
        layout.setSpacing(10)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addStretch()

        self.update_style()

    def update_style(self):
        if self.selected:
            border = theme.PRIMARY
            background = theme.CARD_SELECTED
        else:
            border = theme.BORDER
            background = theme.CARD

        self.setStyleSheet(f"""
            QFrame#optionCard {{
                background-color: {background};
                border: 2px solid {border};
                border-radius: {theme.CARD_RADIUS}px;
            }}

            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

    def set_selected(self, selected: bool):
        self.selected = selected
        self.update_style()

    def enterEvent(self, event):
        if not self.selected:
            self.setStyleSheet(f"""
                QFrame#optionCard {{
                    background-color: {theme.CARD_HOVER};
                    border: 2px solid {theme.PRIMARY};
                    border-radius: {theme.CARD_RADIUS}px;
                }}

                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)

        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)