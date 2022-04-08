from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from shared_widgets import Label, ContentBox

class StockPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)

        self.characteristics = CharacteristicsBox()
        self.layout.addWidget(self.characteristics, 0, 0, 1, 3)

        self.news = NewsBox()
        self.layout.addWidget(self.news, 0, 3, 1, 3)

        self.description = DescriptionBox()
        self.layout.addWidget(self.description, 1, 0, 1, 4)

        self.prices = PriceBox()
        self.layout.addWidget(self.prices, 1, 4, 2, 2)

        self.analysts = AnalystsBox()
        self.layout.addWidget(self.analysts, 2, 0, 1, 1)

        self.value = ValueBox()
        self.layout.addWidget(self.value, 2, 1, 1, 1)

        self.profitability = ProfitabilityBox()
        self.layout.addWidget(self.profitability, 2, 2, 1, 1)

        self.growth = GrowthBox()
        self.layout.addWidget(self.growth, 2, 3, 1, 1)


class CharacteristicsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        
        self.logo = Label()
        self.layout.addWidget(self.logo, 0, 0, 2, 2)

        self.name = Label()
        self.layout.addWidget(self.name, 0, 2, 1, 7)

        self.update_button = QPushButton()
        self.layout.addWidget(self.update_button, 1, 2, 1, 1)

        self.ticker = CharacteristicsItem()
        self.layout.addWidget(self.ticker, 1, 3, 1, 1)

        self.isin = CharacteristicsItem()
        self.layout.addWidget(self.isin, 1, 4, 1, 1)

        self.last_price = CharacteristicsItem()
        self.layout.addWidget(self.last_price, 1, 5, 1, 1)

        self.market_cap = CharacteristicsItem()
        self.layout.addWidget(self.market_cap, 1, 6, 1, 1)

        self.pe_ratio = CharacteristicsItem()
        self.layout.addWidget(self.pe_ratio, 1, 7, 1, 1)

        self.div_yield = CharacteristicsItem()
        self.layout.addWidget(self.div_yield, 1, 8, 1, 1)


class CharacteristicsItem(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.value = Label()
        self.layout.addWidget(self.value)

        self.name = Label()
        self.layout.addWidget(self.name)


class NewsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DescriptionBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PriceBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AnalystsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ValueBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProfitabilityBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GrowthBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)