from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QFileDialog,
)

from ui import theme
from ui.hero_card import HeroCard
from ui.option_card import OptionCard
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

        # Hero Card
        self.hero_card = HeroCard()
        self.layout.addWidget(self.hero_card)

        # Connect Select Folder button
        self.hero_card.browse_button.clicked.connect(self.select_folder)
        
        #drop folder signal
        self.hero_card.folder_dropped.connect(
            lambda folder: self.handle_folder_selected(folder)
        )

        # Option Cards
        self.grid = QGridLayout()
        self.grid.setSpacing(theme.CARD_SPACING)

        self.date_card = OptionCard(
            "📅",
            "Date Template",
            "Year → Month → Day"
        )

        self.type_card = OptionCard(
            "📂",
            "File Type Template",
            "Images • Videos"
        )

        self.templates_card = OptionCard(
            "⭐",
            "My Templates",
            "No saved templates"
        )

        self.duplicates_card = OptionCard(
            "🗑️",
            "Remove Duplicates",
            "Smart Detection"
        )

        self.grid.addWidget(self.date_card, 0, 0)
        self.grid.addWidget(self.type_card, 0, 1)
        self.grid.addWidget(self.templates_card, 1, 0)
        self.grid.addWidget(self.duplicates_card, 1, 1)

        self.layout.addLayout(self.grid)

        self.setLayout(self.layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder"
        )

        if folder:
            self.handle_folder_selected(folder)
            
    def handle_folder_selected(self, folder):
        print(f"Selected Folder: {folder}")
        
        scanner = FolderScanner()
        
        stats = scanner.scan(folder)
        
        print(stats)    
        
    