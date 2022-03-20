from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import queries
from stylesheets import scrollarea_css

class StockPage(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.view = QFrame()
        self.layout = QHBoxLayout(self.view)

        self.layout.addWidget(QFrame())

        self.content = QFrame()
        self.content.layout = QVBoxLayout(self.content)
        self.content.layout.setContentsMargins(50, 0, 0, 50)
        self.content.layout.setSpacing(20)
        self.layout.addWidget(self.content)

        self.layout.addWidget(QFrame())

        self.setWidgetResizable(True)
        self.horizontalScrollBar().setFixedHeight(7)
        self.verticalScrollBar().setFixedWidth(7)
        self.setStyleSheet(scrollarea_css)
        self.setWidget(self.view)

        self.header = MainHeader()
        self.content.layout.addWidget(self.header)
        self.overview_section = OverviewSection()
        self.content.layout.addWidget(self.overview_section)
        self.price_section = PriceSection()
        self.content.layout.addWidget(self.price_section)
        self.fundamentals_section = FundamentalsSection()
        self.content.layout.addWidget(self.fundamentals_section)
        self.holders_section = HoldersSection()
        self.content.layout.addWidget(self.holders_section)
        self.filings_section = FilingsSection()
        self.content.layout.addWidget(self.filings_section)

    def update_data(self, ticker):
        data = queries.get_stock_data(ticker)
        self.header.update_data(data)


class MainHeader(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(20)
        self.layout.setVerticalSpacing(00)

        self.logo = QLabel()
        self.layout.addWidget(self.logo, 0, 0, 2, 2)

        self.name = QLabel()
        self.name.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-weight: Bold;
                font-size: 28px;
            }
            """
        )
        self.layout.addWidget(self.name, 0, 3, 1, 10)

        self.country = MainHeaderItem("Country", "")
        self.layout.addWidget(self.country, 1, 3, 1, 1)
        self.ticker = MainHeaderItem("Ticker", "")
        self.layout.addWidget(self.ticker, 1, 4, 1, 1)
        self.isin = MainHeaderItem("ISIN", "")
        self.layout.addWidget(self.isin, 1, 5, 1, 1)
        self.price = MainHeaderItem("Last Price", "")
        self.layout.addWidget(self.price, 1, 6, 1, 1)
        self.market_cap = MainHeaderItem("Market Cap", "")
        self.layout.addWidget(self.market_cap, 1, 7, 1, 1)
        self.pe = MainHeaderItem("P/E Ratio", "")
        self.layout.addWidget(self.pe, 1, 8, 1, 1)
        self.div_yield = MainHeaderItem("Dividend Yield", "")
        self.layout.addWidget(self.div_yield, 1, 9, 1, 1)
        self.beta = MainHeaderItem("Beta", "")
        self.layout.addWidget(self.beta, 1, 10, 1, 1)
        self.rating = MainHeaderItem("Ø Rating", "")
        self.layout.addWidget(self.rating, 1, 11, 1, 1)
        self.pt = MainHeaderItem("Ø Price Target", "")
        self.layout.addWidget(self.pt, 1, 12, 1, 1)

        placeholder = QFrame()
        placeholder.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.layout.addWidget(placeholder, 0, 13, 2, 1)

        self.updated = MainHeaderItem("Last Updated", "2022-06-02")
        self.layout.addWidget(self.updated, 1, 14, 1, 1)
    
    def update_data(self, data):
        logo = QPixmap()
        logo.loadFromData(data["logo"])
        logo = logo.scaledToHeight(90, Qt.SmoothTransformation)
        self.logo.setPixmap(logo)
        self.name.setText(data["name"])
        country_flag = QPixmap()
        country_flag.loadFromData(data["country_flag"])
        country_flag = country_flag.scaledToHeight(15, Qt.SmoothTransformation)
        self.country.value.setPixmap(country_flag)
        self.ticker.value.setText(data["ticker"])
        self.isin.value.setText(data["isin"])
        self.price.value.setText(str(data["price"]))
        self.market_cap.value.setText(str(data["market_cap"]))
        self.pe.value.setText(str(data["pe"]))
        self.div_yield.value.setText(str(data["div_yield"]))
        self.beta.value.setText(str(data["beta"]))
        self.rating.value.setText(str(data["rating"]))
        self.pt.value.setText(str(data["price_target"]))


class MainHeaderItem(QFrame):
    def __init__(self, item, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.item = QLabel(item)
        self.item.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 12px;
                font-weight: bold;
                color: #AEAEAE;
            }
            """
        )
        self.layout.addWidget(self.item)

        self.value = QLabel(value)
        self.value.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 14px;
                font-weight: bold;
                color: #25282B;
            }
            """
        )
        self.layout.addWidget(self.value)


class OverviewSection(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

class PriceSection(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)


class FundamentalsSection(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)


class HoldersSection(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)


class FilingsSection(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)