from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from shared_widgets import Label, ContentBox

class StockPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)

        self.characteristics_box = CharacteristicsBox()
        self.layout.addWidget(self.characteristics_box, 0, 0, 1, 3)
        self.characteristics_box.setFixedHeight(100)

        self.news_box = NewsBox()
        self.layout.addWidget(self.news_box, 0, 3, 1, 3)

        self.description_box = DescriptionBox()
        self.layout.addWidget(self.description_box, 1, 0, 1, 4)

        self.prices_box = PriceBox()
        self.layout.addWidget(self.prices_box, 1, 4, 2, 2)

        self.analysts_box = AnalystsBox()
        self.layout.addWidget(self.analysts_box, 2, 0, 1, 1)

        self.value_box = ValueBox()
        self.layout.addWidget(self.value_box, 2, 1, 1, 1)

        self.profitability_box = ProfitabilityBox()
        self.layout.addWidget(self.profitability_box, 2, 2, 1, 1)

        self.growth_box = GrowthBox()
        self.layout.addWidget(self.growth_box, 2, 3, 1, 1)


class CharacteristicsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        
        self.logo = Logo()
        self.layout.addWidget(self.logo, 0, 0, 2, 2)

        self.name = Label()
        self.layout.addWidget(self.name, 0, 2, 1, 7)

        self.update_button = QPushButton()
        self.layout.addWidget(self.update_button, 1, 2, 1, 1)

        self.ticker = CharacteristicsItem("Ticker")
        self.layout.addWidget(self.ticker, 1, 3, 1, 1)

        self.isin = CharacteristicsItem("ISIN")
        self.layout.addWidget(self.isin, 1, 4, 1, 1)

        self.last_price = CharacteristicsItem("Last Price")
        self.layout.addWidget(self.last_price, 1, 5, 1, 1)

        self.market_cap = CharacteristicsItem("Market Cap")
        self.layout.addWidget(self.market_cap, 1, 6, 1, 1)

        self.pe_ratio = CharacteristicsItem("P/E Ratio")
        self.layout.addWidget(self.pe_ratio, 1, 7, 1, 1)

        self.div_yield = CharacteristicsItem("Dividend Yield")
        self.layout.addWidget(self.div_yield, 1, 8, 1, 1)

class Logo(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QPixmap()

    @Slot(bytes)
    def update_logo(self, logo):
        self.icon.loadFromData(logo)
        self.setPixmap(self.icon)


class CharacteristicsItem(QFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.value = Label()
        self.layout.addWidget(self.value)

        self.name = Label(name)
        self.layout.addWidget(self.name)


class NewsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.news = []

        self.layout = QHBoxLayout(self)


class DescriptionBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)

        self.address = DescriptionAddress()
        self.layout.addWidget(self.address, 0, 0, 1, 1)

        self.industry = DescriptionIndustry()
        self.layout.addWidget(self.industry, 0, 1, 1, 1)
        
        self.executives = DescriptionExcutives()
        self.layout.addWidget(self.executives, 0, 2, 1, 1)

        self.description = Label()
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignJustify)
        self.layout.addWidget(self.description, 1, 0, 1, 3)


class DescriptionAddress(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.country = Country()
        self.layout.addWidget(self.country)
        
        self.city = Label()
        self.layout.addWidget(self.city)

        self.street = Label()
        self.layout.addWidget(self.street)

        self.website = Label()
        self.layout.addWidget(self.website)

        self.employees = Label()
        self.layout.addWidget(self.employees)

class Country(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QPixmap()

    @Slot(bytes)
    def update_icon(self, logo):
        self.icon.loadFromData(logo)
        self.setIcon(self.icon)


class DescriptionIndustry(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.gics = Label("GICS")
        self.layout.addWidget(self.gics)

        self.gics_sector = QPushButton()
        self.layout.addWidget(self.gics_sector)

        self.gics_industry = QPushButton()
        self.layout.addWidget(self.gics_industry)

        self.sic = Label("SIC")
        self.layout.addWidget(self.sic)

        self.sic_division = QPushButton()
        self.layout.addWidget(self.sic_division)

        self.sic_industry = QPushButton()
        self.layout.addWidget(self.sic_industry)


class DescriptionExcutives(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PriceBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AnalystsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.abr = None
        self.average_price_target = None
        self.lowest_price_target = None
        self._highest_target = None


class FactorBoxItem(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.value = Label()
        self.layout.addWidget(self.value)

        self.name = Label()
        self.layout.addWidget(self.name)


class ValueBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.header = Label("Value")
        self.layout.addWidget(self.header)

        self.ey = FactorBoxItem()
        self.layout.addWidget(self.ey)

        self.pb = FactorBoxItem()
        self.layout.addWidget(self.pb)

        self.ps = FactorBoxItem()
        self.layout.addWidget(self.ps)


class ProfitabilityBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.header = Label("Profitability")
        self.layout.addWidget(self.header)

        self.roe = FactorBoxItem()
        self.layout.addWidget(self.roe)

        self.roa = FactorBoxItem()
        self.layout.addWidget(self.roa)

        self.margin = FactorBoxItem()
        self.layout.addWidget(self.margin)


class GrowthBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.header = Label("Growth")
        self.layout.addWidget(self.header)
        
        self.earnings_growth = FactorBoxItem()
        self.layout.addWidget(self.earnings_growth)

        self.revenue_growth = FactorBoxItem()
        self.layout.addWidget(self.revenue_growth)

        self.reinvestment_rate = FactorBoxItem()
        self.layout.addWidget(self.reinvestment_rate)