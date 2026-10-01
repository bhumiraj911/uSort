from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)

from ui import theme


class PreviewPage(QWidget):

    back_requested = Signal()

    organize_requested = Signal()

    def __init__(self):
        super().__init__()

        self.selected_categories = []

        self.folder_names = {}

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

        self.title_label = QLabel("Preview")

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

        self.subtitle_label = QLabel("Review how your files will be organized")

        self.subtitle_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 14px;
        """)

        self.layout.addWidget(self.subtitle_label)

        # Preview container

        self.preview_container = QWidget()

        self.preview_layout = QVBoxLayout(self.preview_container)

        self.preview_layout.setSpacing(10)

        self.preview_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.layout.addWidget(self.preview_container)

        self.layout.addStretch()

        # Bottom buttons

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.organize_button = QPushButton("Organize →")

        self.organize_button.setCursor(Qt.PointingHandCursor)

        self.organize_button.setFixedHeight(44)

        self.organize_button.clicked.connect(self.organize_requested.emit)

        self.organize_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding-left: 24px;
                padding-right: 24px;
            }}

            QPushButton:hover {{
                background-color: #2563EB;
            }}
        """)

        button_layout.addWidget(self.organize_button)

        self.layout.addLayout(button_layout)

    def set_preview(
        self,
        selected_categories,
        folder_names,
        stats,
    ):

        self.selected_categories = selected_categories

        self.folder_names = folder_names

        self.clear_preview()

        total_files = 0

        category_keys = {
            "Documents": "documents",
            "Images": "images",
            "Videos": "videos",
            "Audio": "audio",
            "Archives": "archives",
            "Others": "others",
            "No Extension": "no_extension",
        }

        for item in selected_categories:

            category = item["category"]

            extensions = item["extensions"]

            category_count = 0

            category_key = category_keys.get(
                category,
                category,
            )

            category_stats = stats.get(
                category_key,
                {},
            )

            for extension in extensions:

                category_count += category_stats.get(
                    extension,
                    0,
                )

            total_files += category_count

            destination = folder_names.get(
                category,
                category,
            )

            self.add_preview_row(
                category,
                destination,
                category_count,
            )

        self.add_summary(total_files)

    def add_preview_row(
        self,
        category,
        destination,
        file_count,
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

        category_label = QLabel(category)

        category_label.setStyleSheet(f"""
            color: {theme.TEXT};
            font-size: 15px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)

        arrow_label = QLabel("→")

        arrow_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 18px;
            background: transparent;
            border: none;
        """)

        destination_label = QLabel(destination)

        destination_label.setStyleSheet(f"""
            color: {theme.TEXT};
            font-size: 15px;
            background: transparent;
            border: none;
        """)

        count_label = QLabel(f"{file_count} files")

        count_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 13px;
            background: transparent;
            border: none;
        """)

        layout.addWidget(category_label)

        layout.addStretch()

        layout.addWidget(arrow_label)

        layout.addSpacing(12)

        layout.addWidget(destination_label)

        layout.addSpacing(20)

        layout.addWidget(count_label)

        self.preview_layout.addWidget(row)

    def add_summary(
        self,
        total_files,
    ):

        summary = QLabel(f"Total files: {total_files}")

        summary.setStyleSheet(f"""
            color: {theme.TEXT};
            font-size: 16px;
            font-weight: 600;
            padding-top: 10px;
        """)

        self.preview_layout.addWidget(summary)

    def clear_preview(self):

        while self.preview_layout.count() > 0:

            item = self.preview_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()
