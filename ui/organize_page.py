from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QCheckBox,
    QPushButton,
    QScrollArea,
)

from ui import theme


class CategoryRow(QFrame):

    selection_changed = Signal()

    def __init__(
        self,
        category: str,
        files: dict,
        icon: str,
    ):
        super().__init__()

        self.category = category
        self.files = files
        self.expanded = False

        self.setObjectName("categoryRow")

        # Main Layout

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        self.main_layout.setSpacing(8)

        # Header

        self.header = QHBoxLayout()
        self.header.setSpacing(10)

        # Expand button

        self.expand_button = QPushButton("▶")
        self.expand_button.setFixedSize(28, 28)
        self.expand_button.setCursor(Qt.PointingHandCursor)

        self.expand_button.clicked.connect(self.toggle_expanded)

        # Category checkbox

        self.checkbox = QCheckBox()

        self.checkbox.clicked.connect(self.category_checkbox_changed)

        # Icon

        self.icon_label = QLabel(icon)

        self.icon_label.setStyleSheet("""
            font-size: 22px;
            background: transparent;
        """)

        # Category name

        self.name_label = QLabel(category)

        self.name_label.setStyleSheet(f"""
            color: {theme.TEXT};
            font-size: 15px;
            font-weight: 600;
            background: transparent;
        """)

        # Count

        self.count_label = QLabel(str(sum(files.values())))

        self.count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.count_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 13px;
            background: transparent;
        """)

        self.header.addWidget(self.expand_button)

        self.header.addWidget(self.checkbox)

        self.header.addWidget(self.icon_label)

        self.header.addWidget(self.name_label)

        self.header.addStretch()

        self.header.addWidget(self.count_label)

        self.main_layout.addLayout(self.header)

        # Extensions

        self.extensions_widget = QWidget()

        self.extensions_layout = QVBoxLayout(self.extensions_widget)

        self.extensions_layout.setContentsMargins(
            66,
            4,
            10,
            4,
        )

        self.extensions_layout.setSpacing(5)

        self.extension_checkboxes = {}

        for extension, count in sorted(
            files.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            extension_checkbox = QCheckBox(f"{extension.upper()}   ({count})")

            extension_checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {theme.SECONDARY_TEXT};
                    font-size: 13px;
                    background: transparent;
                }}
            """)

            extension_checkbox.stateChanged.connect(self.extension_changed)

            self.extensions_layout.addWidget(extension_checkbox)

            self.extension_checkboxes[extension] = extension_checkbox

        self.extensions_widget.hide()

        self.main_layout.addWidget(self.extensions_widget)

        self.update_style()

    # Expand / Collapse

    def toggle_expanded(self):

        self.expanded = not self.expanded

        if self.expanded:

            self.expand_button.setText("▼")

            self.extensions_widget.show()

        else:

            self.expand_button.setText("▶")

            self.extensions_widget.hide()

    # Category Selection

    def category_checkbox_changed(
        self,
        checked,
    ):

        for checkbox in self.extension_checkboxes.values():

            checkbox.blockSignals(True)

            checkbox.setChecked(checked)

            checkbox.blockSignals(False)

        self.selection_changed.emit()

    # Extension Selection

    def extension_changed(self):

        checkboxes = list(self.extension_checkboxes.values())

        if not checkboxes:
            return

        checked_count = sum(checkbox.isChecked() for checkbox in checkboxes)

        self.checkbox.blockSignals(True)

        if checked_count == len(checkboxes):

            self.checkbox.setCheckState(Qt.Checked)

        elif checked_count == 0:

            self.checkbox.setCheckState(Qt.Unchecked)

        else:

            self.checkbox.setCheckState(Qt.PartiallyChecked)

        self.checkbox.blockSignals(False)

        self.selection_changed.emit()

    # Styling

    def update_style(self):

        self.setStyleSheet(f"""
            QFrame#categoryRow {{
                background-color: {theme.CARD};
                border: 1px solid {theme.BORDER};
                border-radius: {theme.CARD_RADIUS}px;
            }}

            QPushButton {{
                background: transparent;
                border: none;
                color: {theme.SECONDARY_TEXT};
                font-size: 12px;
            }}

            QPushButton:hover {{
                color: {theme.TEXT};
            }}

            QCheckBox {{
                background: transparent;
            }}
        """)


class OrganizePage(QWidget):

    back_requested = Signal()
    continue_requested = Signal()

    CATEGORY_INFO = {
        "documents": (
            "📄",
            "Documents",
        ),
        "images": (
            "🖼️",
            "Images",
        ),
        "videos": (
            "🎥",
            "Videos",
        ),
        "audio": (
            "🎵",
            "Audio",
        ),
        "archives": (
            "🗜️",
            "Archives",
        ),
        "others": (
            "📦",
            "Others",
        ),
        "no_extension": (
            "📄",
            "No Extension",
        ),
    }

    def __init__(self):
        super().__init__()

        self.stats = {}

        self.setup_ui()

    def setup_ui(self):

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        self.layout.setSpacing(theme.CARD_SPACING)

        # Top Bar

        top_bar = QHBoxLayout()

        self.back_button = QPushButton("← Back")

        self.back_button.setCursor(Qt.PointingHandCursor)

        self.back_button.clicked.connect(self.back_requested.emit)

        self.title_label = QLabel("Select")

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

        self.subtitle_label = QLabel("Choose what you want to organize")

        self.subtitle_label.setStyleSheet(f"""
            color: {theme.SECONDARY_TEXT};
            font-size: 14px;
        """)

        self.layout.addWidget(self.subtitle_label)

        # Categories Container

        self.categories_container = QWidget()

        self.categories_layout = QVBoxLayout(self.categories_container)

        self.categories_layout.setSpacing(10)

        self.categories_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.categories_scroll = QScrollArea()

        self.categories_scroll.setWidgetResizable(True)

        self.categories_scroll.setFrameShape(QFrame.NoFrame)

        self.categories_scroll.setWidget(self.categories_container)

        self.layout.addWidget(
            self.categories_scroll,
            1,
        )

        # Continue Button

        self.continue_button = QPushButton("Continue →")

        self.continue_button.setCursor(Qt.PointingHandCursor)

        self.continue_button.setFixedHeight(44)

        self.continue_button.setEnabled(False)

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

            QPushButton:disabled {{
                background-color: {theme.BORDER};
                color: {theme.SECONDARY_TEXT};
            }}
        """)

        self.layout.addWidget(self.continue_button)

    # Load Scanner Data

    def set_stats(
        self,
        stats,
    ):

        self.stats = stats

        self.clear_categories()

        for category, (
            icon,
            display_name,
        ) in self.CATEGORY_INFO.items():

            files = stats.get(category)

            if not files:
                continue

            row = CategoryRow(
                display_name,
                files,
                icon,
            )

            row.selection_changed.connect(self.update_continue_state)

            self.categories_layout.addWidget(row)

        self.update_continue_state()

    # Clear Existing Categories

    def clear_categories(self):

        while self.categories_layout.count() > 0:

            item = self.categories_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    # Continue State

    def update_continue_state(
        self,
    ):

        has_selection = False

        for index in range(self.categories_layout.count()):

            item = self.categories_layout.itemAt(index)

            widget = item.widget()

            if not isinstance(
                widget,
                CategoryRow,
            ):
                continue

            if widget.checkbox.isChecked() or any(
                checkbox.isChecked()
                for checkbox in widget.extension_checkboxes.values()
            ):

                has_selection = True

                break

        self.continue_button.setEnabled(has_selection)

    def get_selected_categories(
        self,
    ):

        selected_categories = []

        for index in range(self.categories_layout.count()):

            item = self.categories_layout.itemAt(index)

            widget = item.widget()

            if not isinstance(
                widget,
                CategoryRow,
            ):
                continue

            selected_extensions = []

            for (
                extension,
                checkbox,
            ) in widget.extension_checkboxes.items():

                if checkbox.isChecked():

                    selected_extensions.append(extension)

            if selected_extensions:

                selected_categories.append(
                    {
                        "category": widget.category,
                        "extensions": selected_extensions,
                    }
                )

        return selected_categories
