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
        self.scroll.setVerticalScrollBarPolicy(
    Qt.ScrollBarAsNeeded)
        
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

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

        section = QLabel(title)

        section.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {theme.TEXT};
        """)

        self.content_layout.addWidget(section)

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
    
    
    def update_stats(self, stats):
        
    
        self.clear_content()

        self.add_row("Files", stats["total_files"])
        self.add_row("Folders", stats["total_folders"])
        self.add_row("Size", self.format_size(stats["total_size"]))

        for category, files in stats.items():

            if category in [
                "total_files",
                "total_folders",
                "total_size",
            ]:
                continue

            self.add_section(category.capitalize())

            for extension, count in files.items():

                self.add_row(
                    extension.upper(),
                    count,
                )
                
        self.content.adjustSize()
               