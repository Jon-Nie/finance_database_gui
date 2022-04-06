from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from finance_database_gui.shared_widgets import ContentBox

class StockPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)

        self.name = ContentBox(self)
        self.layout.addWidget(self.name, 0, 0, 1, 3)
        self.name.setMaximumHeight(50)

        self.news = ContentBox(self)
        self.layout.addWidget(self.news, 0, 3, 1, 3)

        self.description = ContentBox(self)
        self.layout.addWidget(self.description, 1, 0, 1, 4)

        self.prices = ContentBox(self)
        self.layout.addWidget(self.prices, 1, 4, 2, 2)

        self.analysts = ContentBox(self)
        self.layout.addWidget(self.analysts, 2, 0, 1, 1)

        self.value = ContentBox(self)
        self.layout.addWidget(self.value, 2, 1, 1, 1)

        self.profitability = ContentBox(self)
        self.layout.addWidget(self.profitability, 2, 2, 1, 1)
        self.profitability.setMaximumWidth(50)

        self.growth = ContentBox(self)
        self.layout.addWidget(self.growth, 2, 3, 1, 1)