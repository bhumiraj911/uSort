from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from ui import theme


class StatsCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setObjectName("statsCard")
        self.setMinimumHeight(450)
        self.setMaximumHeight(850)

        self.setStyleSheet(f"""
            QFrame#statsCard {{
                background-color: {theme.CARD};
                border: 1px solid {theme.BORDER};
                border-radius: {theme.CARD_RADIUS}px;
            }}

            QLabel {{
                background: transparent;
                border: none;
                color: {theme.TEXT};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QWidget()

        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(
            30,
            25,
            30,
            25,
        )
        self.content_layout.setSpacing(20)

        self.title = QLabel("Folder Summary")
        self.title.setStyleSheet(f"""
            font-size: 22px;
            font-weight: 600;
            color: {theme.TEXT};
        """)

        self.content_layout.addWidget(self.title)

        self.scroll.setWidget(self.content)

        main_layout.addWidget(self.scroll)

    def add_section(self, title):

        icon = self.get_category_icon(title)

        section = QLabel(f"{icon} {title}")

        section.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {theme.TEXT};
        """)

        self.content_layout.addWidget(section)

    def add_separator(self):

        separator = QFrame()

        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        separator.setStyleSheet(f"""
            color: {theme.BORDER};
            background-color: {theme.BORDER};
            border: none;
            max-height: 1px;
        """)

        self.content_layout.addWidget(separator)

    def add_row(self, label, value):

        row = QWidget()

        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)

        left = QLabel(label)

        right = QLabel(str(value))
        right.setAlignment(Qt.AlignmentFlag.AlignRight)

        left.setStyleSheet(f"""
            font-size: 14px;
            color: {theme.SECONDARY_TEXT};
        """)

        right.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {theme.TEXT};
        """)

        layout.addWidget(left)
        layout.addStretch()
        layout.addWidget(right)

        self.content_layout.addWidget(row)

    def clear_content(self):

        while self.content_layout.count() > 1:

            item = self.content_layout.takeAt(1)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def format_size(self, size):

        units = ["B", "KB", "MB", "GB", "TB"]

        index = 0

        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1

        if units[index] == "B":
            return f"{int(size)} B"

        return f"{size:.2f} {units[index]}"

    def update_stats(self, stats, folder_name):

        self.clear_content()

        self.title.setText(f"Data present in {folder_name}")

        # Summary
        self.add_row("Files", stats["total_files"])
        self.add_row("Folders", stats["total_folders"])
        self.add_row("Size", self.format_size(stats["total_size"]))

        self.add_separator()

        # Category order
        category_order = [
            "documents",
            "images",
            "videos",
            "audio",
            "archives",
            "others",
            "no_extension",
        ]

        for category in category_order:

            files = stats.get(category)

            if not files:
                continue

            if category == "no_extension":
                self.add_section("No Extension")
            else:
                self.add_section(category.capitalize())

            if category == "no_extension":
                self.add_row("Files", sum(files.values()))
            else:
                for extension, count in sorted(
                    files.items(),
                    key=lambda item: item[1],
                    reverse=True,
                ):
                    self.add_row(
                        extension.upper(),
                        count,
                    )

            self.add_separator()

        self.content.adjustSize()

    def get_category_icon(self, category):

        icons = {
            "documents": "📄",
            "images": "🖼️",
            "videos": "🎥",
            "audio": "🎵",
            "archives": "🗜️",
            "others": "📦",
            "no_extension": "📄",
            "no extension": "📄",
        }

        return icons.get(category.lower(), "📦")
