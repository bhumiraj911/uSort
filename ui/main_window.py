from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QHBoxLayout,
    QFileDialog,
    QStackedWidget,
)

from pathlib import Path

from ui import theme
from ui.hero_card import HeroCard
from ui.option_card import OptionCard
from ui.stats_card import StatsCard
from ui.organize_page import OrganizePage
from ui.organization_method_page import OrganizationMethodPage
from ui.file_type_page import FileTypePage
from ui.category_organization_page import CategoryOrganizationPage

from core.scanner import FolderScanner


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_window()
        self.setup_layout()

    def setup_window(self):

        self.setWindowTitle("uSort")

        self.resize(1200, 800)

        self.setMinimumSize(1000, 700)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.BACKGROUND};
                color: {theme.TEXT};
                font-family: "{theme.FONT}";
            }}
        """)

    def setup_layout(self):

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            theme.PADDING,
            theme.PADDING,
            theme.PADDING,
            theme.PADDING,
        )

        self.layout.setSpacing(theme.CARD_SPACING)

        # Hero card

        self.hero_card = HeroCard()

        self.layout.addWidget(self.hero_card)

        # Page stack

        self.pages = QStackedWidget()

        self.dashboard_page = QWidget()

        self.organize_page = OrganizePage()

        self.organization_method_page = OrganizationMethodPage()

        self.file_type_page = FileTypePage()

        self.category_organization_page = CategoryOrganizationPage()

        # Dashboard page

        self.content_layout = QHBoxLayout(self.dashboard_page)

        self.content_layout.setSpacing(theme.CARD_SPACING)

        # Stats card

        self.stats_card = StatsCard()

        self.stats_card.hide()

        self.content_layout.addWidget(
            self.stats_card,
            1,
        )

        # Option cards

        self.grid = QGridLayout()

        self.grid.setSpacing(theme.CARD_SPACING)

        self.organize_card = OptionCard(
            "📂",
            "Organize",
            "Organize your files",
        )

        self.duplicates_card = OptionCard(
            "🗑️",
            "Remove Duplicates",
            "Smart Detection",
        )

        self.templates_card = OptionCard(
            "⭐",
            "My Templates",
            "No saved templates",
        )

        self.grid.addWidget(
            self.organize_card,
            0,
            0,
        )

        self.grid.addWidget(
            self.duplicates_card,
            0,
            1,
        )

        self.grid.addWidget(
            self.templates_card,
            1,
            0,
        )

        self.content_layout.addLayout(self.grid)

        # Add pages

        self.pages.addWidget(self.dashboard_page)

        self.pages.addWidget(self.organize_page)

        self.pages.addWidget(self.organization_method_page)

        self.pages.addWidget(self.file_type_page)

        self.pages.addWidget(self.category_organization_page)

        self.layout.addWidget(self.pages)

        # Connections

        # Select folder button

        self.hero_card.browse_button.clicked.connect(self.select_folder)

        # Drop folder signal

        self.hero_card.folder_dropped.connect(
            lambda folder: self.handle_folder_selected(folder)
        )

        # Organize card

        self.organize_card.clicked.connect(self.open_organize)

        # Back to dashboard

        self.organize_page.back_requested.connect(self.back_to_dashboard)

        # Continue to organization method

        self.organize_page.continue_requested.connect(self.open_organization_method)

        # Back to organize page

        self.organization_method_page.back_requested.connect(self.back_to_organize)

        # Open file type page

        self.organization_method_page.file_type_selected.connect(self.open_file_type)

        # Back to organization method

        self.file_type_page.back_requested.connect(self.back_to_organization_method)

        # File type selection

        self.file_type_page.category_selected.connect(self.open_category_organization)

        # Back to file type

        self.category_organization_page.back_requested.connect(self.back_to_file_type)

        self.setLayout(self.layout)

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
        )

        if folder:

            self.handle_folder_selected(folder)

    def handle_folder_selected(
        self,
        folder,
    ):

        print(f"Selected Folder: {folder}")

        scanner = FolderScanner()

        stats = scanner.scan(folder)

        self.current_stats = stats

        self.organize_page.set_stats(stats)

        folder_name = Path(folder).name

        self.stats_card.update_stats(
            stats,
            folder_name,
        )

        self.stats_card.show()

        self.stats_card.update()

        self.stats_card.repaint()

    def open_organize(self):

        self.pages.setCurrentWidget(self.organize_page)

    def back_to_dashboard(self):

        self.pages.setCurrentWidget(self.dashboard_page)

    def open_organization_method(self):

        self.selected_categories = self.organize_page.get_selected_categories()

        print(
            "Selected categories:",
            self.selected_categories,
        )

        self.pages.setCurrentWidget(self.organization_method_page)

    def back_to_organize(self):

        self.pages.setCurrentWidget(self.organize_page)

    def open_file_type(self):

        self.pages.setCurrentWidget(self.file_type_page)

    def back_to_organization_method(self):

        self.pages.setCurrentWidget(self.organization_method_page)

    def open_category_organization(self):

        self.category_organization_page.set_categories(self.selected_categories)

        self.pages.setCurrentWidget(self.category_organization_page)

    def back_to_file_type(self):

        self.pages.setCurrentWidget(self.file_type_page)
