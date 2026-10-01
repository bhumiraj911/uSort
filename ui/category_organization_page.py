from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFrame,
)

from ui import theme


class CategoryOrganizationPage(QWidget):

    back_requested = Signal()

    continue_requested = Signal()

    def __init__(self):
        super().__init__()

        self.selected_categories = []

        self.folder_inputs = {}

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

        self.title_label = QLabel("Organize by Category")

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

        self.subtitle_label = QLabel("Customize the destination folder names")

        self.subtitle_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 14px;
        """)

        self.layout.addWidget(self.subtitle_label)

        # Categories container

        self.categories_container = QWidget()

        self.categories_layout = QVBoxLayout(self.categories_container)

        self.categories_layout.setSpacing(10)

        self.categories_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.layout.addWidget(self.categories_container)

        self.layout.addStretch()

        # Continue button

        self.continue_button = QPushButton("Continue →")

        self.continue_button.setCursor(Qt.PointingHandCursor)

        self.continue_button.setFixedHeight(44)

        self.continue_button.clicked.connect(self.continue_requested.emit)

        self.continue_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background-color: #2563EB;
            }}
        """)

        self.layout.addWidget(self.continue_button)

    def set_categories(
        self,
        selected_categories,
    ):

        self.selected_categories = selected_categories

        self.clear_categories()

        self.folder_inputs = {}

        for item in selected_categories:

            category = item["category"]

            self.add_category_row(category)

    def add_category_row(
        self,
        category,
    ):

        row = QFrame()

        row.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.CARD};
                border: 1px solid {theme.BORDER};
                border-radius: {theme.CARD_RADIUS}px;
            }}
        """)

        layout = QHBoxLayout(row)

        layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        # Category name

        category_label = QLabel(category)

        category_label.setStyleSheet(f"""
            color: {theme.TEXT};
            font-size: 15px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)

        # Arrow

        arrow_label = QLabel("→")

        arrow_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 18px;
            background: transparent;
            border: none;
        """)

        # Folder input

        folder_input = QLineEdit(category)

        folder_input.setMinimumWidth(200)

        folder_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {theme.BACKGROUND};
                color: {theme.TEXT};
                border: 1px solid {theme.BORDER};
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                border: none;
            }}

            QLineEdit:focus {{
                border: 1px solid {theme.PRIMARY};
            }}
        """)

        self.folder_inputs[category] = folder_input

        layout.addWidget(category_label)

        layout.addStretch()

        layout.addWidget(arrow_label)

        layout.addSpacing(12)

        layout.addWidget(folder_input)

        self.categories_layout.addWidget(row)

    def clear_categories(self):

        while self.categories_layout.count() > 0:

            item = self.categories_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

    def get_folder_names(self):

        folder_names = {}

        for (
            category,
            input_field,
        ) in self.folder_inputs.items():

            folder_names[category] = input_field.text().strip()

        return folder_names
