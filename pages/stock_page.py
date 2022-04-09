from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from shared_widgets import Label, ContentBox

class StockPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 50, 50, 50)

        self.upper_layout = QHBoxLayout()
        self.layout.addLayout(self.upper_layout)
        self.lower_layout = QGridLayout()
        self.layout.addLayout(self.lower_layout)

        self.characteristics_box = CharacteristicsBox()
        self.upper_layout.addWidget(self.characteristics_box, 0)
        self.characteristics_box.setFixedHeight(120)

        self.news_box = NewsBox()
        self.news_box.setMaximumWidth(9999)
        self.news_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.upper_layout.addWidget(self.news_box, 1)

        self.description_box = DescriptionBox()
        self.lower_layout.addWidget(self.description_box, 0, 0, 1, 4)

        self.prices_box = PriceBox()
        self.lower_layout.addWidget(self.prices_box, 0, 4, 2, 1)

        self.analysts_box = AnalystsBox()
        self.lower_layout.addWidget(self.analysts_box, 1, 0, 1, 1)

        self.value_box = ValueBox()
        self.lower_layout.addWidget(self.value_box, 1, 1, 1, 1)

        self.profitability_box = ProfitabilityBox()
        self.lower_layout.addWidget(self.profitability_box, 1, 2, 1, 1)

        self.growth_box = GrowthBox()
        self.lower_layout.addWidget(self.growth_box, 1, 3, 1, 1)

class CharacteristicsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.setContentsMargins(20, 10, 20, 10)
        self.layout.setVerticalSpacing(10)
        
        self.logo = Logo()
        self.layout.addWidget(self.logo, 0, 0, 2, 2)

        self.name = Label()
        self.layout.addWidget(self.name, 0, 2, 1, 7)
        self.name.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 26px;
                font-weight: 900;
                color: #333333
            }
            """
        )

        self.ticker = CharacteristicsItem("Ticker")
        self.layout.addWidget(self.ticker, 1, 2, 1, 1)

        self.isin = CharacteristicsItem("ISIN")
        self.layout.addWidget(self.isin, 1, 3, 1, 1)

        self.last_price = CharacteristicsItem("Last Price")
        self.layout.addWidget(self.last_price, 1, 4, 1, 1)

        self.market_cap = CharacteristicsItem("Market Cap")
        self.layout.addWidget(self.market_cap, 1, 5, 1, 1)

        self.pe_ratio = CharacteristicsItem("P/E Ratio")
        self.layout.addWidget(self.pe_ratio, 1, 6, 1, 1)

        self.payout_yield = CharacteristicsItem("Payout Yield")
        self.layout.addWidget(self.payout_yield, 1, 7, 1, 1)

        self.update_button = QPushButton()
        self.layout.addWidget(self.update_button, 1, 8, 1, 1)

class Logo(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QPixmap()

    @Slot(bytes)
    def update_logo(self, logo):
        self.icon.loadFromData(logo)
        if self.icon.height() > 80:
            self.icon = self.icon.scaledToHeight(80, Qt.SmoothTransformation)
        self.setPixmap(self.icon)


class CharacteristicsItem(QFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.value = Label()
        self.value.setObjectName("value")
        self.layout.addWidget(self.value)

        self.name = Label(name)
        self.name.setObjectName("name")
        self.layout.addWidget(self.name)

        self.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 13px;
            }
            QLabel#value {
                font-weight: 900;
                color: #333333
            }
            QLabel#name {
                font-weight: 900;
                color: #9C9C9C
            }
            """
        )


class NewsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.news = []

        self.layout = QHBoxLayout(self)


class DescriptionBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(0)

        self.address = DescriptionAddress()
        self.layout.addWidget(self.address, 0, 0, 1, 1)

        self.industry = DescriptionIndustry()
        self.layout.addWidget(self.industry, 0, 1, 1, 1)
        
        self.executives = DescriptionExcutives()
        self.layout.addWidget(self.executives, 0, 2, 1, 1)

        self.description = BusinessDescription()
        self.layout.addWidget(self.description, 1, 0, 1, 3)


class BusinessDescription(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWidgetResizable(True)

        self.description = Label()
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignJustify)
        self.description.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 14px;
                font-weight: 400;
                color: #333333;
                padding-left: 10px;
                padding-right: 20px
            }
            """
        )
        self.setWidget(self.description)


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

        self.layout.addWidget(QFrame())

        self.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 14px;
                font-weight: 500;
                color: #333333
            }
            """
        )

class Country(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QPixmap()

        self.setStyleSheet(
            """
            QPushButton {
                font-family: Lato;
                font-size: 14px;
                font-weight: 500;
                color: #333333;
                text-align: left
            }
            """
        )

    @Slot(bytes)
    def update_icon(self, logo):
        self.icon.loadFromData(logo)
        self.setIconSize(QSize(40, 20))
        self.setIcon(self.icon)


class DescriptionIndustry(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.gics = Label("GICS")
        self.gics.setObjectName("header")
        self.layout.addWidget(self.gics)

        self.gics_sector = Label()
        self.gics_sector.setObjectName("value")
        self.layout.addWidget(self.gics_sector)

        self.gics_industry = Label()
        self.gics_industry.setObjectName("value")
        self.layout.addWidget(self.gics_industry)

        self.placeholder = QFrame()
        self.placeholder.setFixedHeight(20)
        self.layout.addWidget(self.placeholder)

        self.sic = Label("SIC")
        self.sic.setObjectName("header")
        self.layout.addWidget(self.sic)

        self.sic_division = Label()
        self.sic_division.setObjectName("value")
        self.layout.addWidget(self.sic_division)

        self.sic_industry = Label()
        self.sic_industry.setObjectName("value")
        self.layout.addWidget(self.sic_industry)

        self.setStyleSheet(
            """
            QLabel {
                font-family: Lato
            }
            QLabel#header {
                font-size: 16px;
                font-weight: 900;
                color: #7E7E7E
            }
            QLabel#value {
                font-size: 14px;
                font-weight: 500;
                color: #333333
            }
            """
        )


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