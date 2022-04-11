from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from shared_widgets import Label, ContentBox

class StockPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(50, 50, 50, 50)

        self.upper_layout = QHBoxLayout()
        self.layout.addLayout(self.upper_layout)
        self.lower_layout = QGridLayout()
        self.layout.addLayout(self.lower_layout)

        self.characteristics_box = CharacteristicsBox()
        self.upper_layout.addWidget(self.characteristics_box, 0)

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

        self.value_box = ValueBox("Value", "Earnings Yield", "Price-to-Book", "Price-to-Sales")
        self.lower_layout.addWidget(self.value_box, 1, 1, 1, 1)

        self.profitability_box = ProfitabilityBox("Profitability", "Return on Equity", "Return on Assets", "Net Margin")
        self.lower_layout.addWidget(self.profitability_box, 1, 2, 1, 1)

        self.growth_box = GrowthBox("Growth (3yr)", "Revenue Growth", "Earnings Growth", "Reinvestment Rate")
        self.lower_layout.addWidget(self.growth_box, 1, 3, 1, 1)

class CharacteristicsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(120)

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
                font-size: 22px;
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
        self.setStyleSheet("Qlabel {margin-right:20px}")

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
        self.setFixedHeight(120)

        self.news = []

        self.layout = QHBoxLayout(self)


class DescriptionBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(20)

        self.address = DescriptionAddress()
        self.layout.addWidget(self.address, 0, 0, 1, 1)

        self.industry = DescriptionIndustry()
        self.layout.addWidget(self.industry, 0, 1, 1, 1)
        
        self.executives = DescriptionExcutives()
        self.layout.addWidget(self.executives, 0, 2, 1, 1)

        self.separator = QFrame()
        self.separator.setFixedHeight(1)
        self.separator.setStyleSheet(
            """
            QFrame {
                background-color: #BCBCBC;
                margin-left: 10px;
                margin-right: 10px
            }
            """
        )
        self.layout.addWidget(self.separator, 1, 0, 1, 3)

        self.description = BusinessDescription()
        self.layout.addWidget(self.description, 2, 0, 1, 3)


class BusinessDescription(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setSingleStep(2)

        self.description = Label()
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignJustify)
        self.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 14px;
                font-weight: 400;
                color: #333333;
                padding-left: 10px;
                padding-right: 20px
            }
            QScrollBar:vertical {
                background-color: #FFFFFF;
                border-radius: 1px;
                width: 5px;
            }
            QScrollBar::handle:vertical {
                background: #C4C4C4;
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
        self.setFixedSize(200, 275)

        self.abr = None
        self.average_price_target = None
        self.lowest_price_target = None
        self._highest_target = None


class FactorBoxItem(QFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.value = Label()
        self.value.setObjectName("value")
        self.value.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.value)

        self.name = Label(name)
        self.name.setObjectName("name")
        self.name.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.name)

        self.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-weight: 600
            }
            QLabel#value {
                font-size: 14px;
                text-align: right;
                color: #333333;
            }
            QLabel#name {
                font-size: 12px;
                color: #696969
            }
            """
        )


class FactorBox(ContentBox):
    def __init__(self, header, var1, var2, var3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(180, 260)
        self.color = "black"

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.placeholder = QFrame()
        self.placeholder.setStyleSheet("background-color: transparent")
        self.placeholder.setFixedHeight(20)
        self.layout.addWidget(self.placeholder)

        self.header = Label()
        self.header.setText(header)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet(
            """
            QLabel {
                background-color: transparent;
                font-family: Lato;
                font-size: 18px;
                font-weight: 600;
                color: #333333
            }
            """
        )
        self.layout.addWidget(self.header)

        self.placeholder2 = QFrame()
        self.placeholder2.setFixedHeight(20)
        self.layout.addWidget(self.placeholder2)

        self.var1 = FactorBoxItem(var1)
        self.layout.addWidget(self.var1)

        self.var2 = FactorBoxItem(var2)
        self.layout.addWidget(self.var2)

        self.var3 = FactorBoxItem(var3)
        self.layout.addWidget(self.var3)

        self.placeholder3 = QFrame()
        self.placeholder3.setFixedHeight(20)
        self.layout.addWidget(self.placeholder3)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.color))

        painter.drawRect(QRectF(10, 0, self.width()-20, 10))
        painter.drawChord(QRectF(0, 0, 20, 20), -180*16, -180*16)
        painter.drawChord(QRectF(self.width()-20, 0, 20, 20), -180*16, -180*16)

        painter.end()


class ValueBox(FactorBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Slot(bytes)
    def update_data(self, ey, pb, ps):
        score = 0
        if ey > 0.05:
            score +=1
        elif ey < 0.3:
            score -= 1
        if pb < 2:
            score +=1
        elif pb > 5:
            score -= 1
        if ps < 2:
            score +=1
        elif ps > 5:
            score -= 1

        if score >= 1:
            self.color = "#5FB538"
        elif score < -1:
            self.color = "#AE3D3D"
        else:
            self.color = "#FFD43C"
        
        self.var1.value.setText(f"{ey:.2%}")
        self.var2.value.setText(f"{pb:.2f}")
        self.var3.value.setText(f"{ps:.2f}")


class ProfitabilityBox(FactorBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Slot(bytes)
    def update_data(self, roe, roa, margin):
        score = 0
        if roe > 0.15:
            score +=1
        elif roe < 0.08:
            score -= 1
        if roa > 0.1:
            score +=1
        elif roa < 0.05:
            score -= 1
        if margin > 0.1:
            score +=1
        elif margin < 0.03:
            score -= 1

        if score >= 1:
            self.color = "#5FB538"
        elif score < -1:
            self.color = "#AE3D3D"
        else:
            self.color = "#FFD43C"
        self.var1.value.setText(f"{roe:.2%}")
        self.var2.value.setText(f"{roa:.2%}")
        self.var3.value.setText(f"{margin:.2%}")


class GrowthBox(FactorBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Slot(bytes)
    def update_data(self, rg, eg, rr):
        score = 0
        if rg > 0.1:
            score +=1
        elif rg < 0:
            score -= 1
        if eg > 0.1:
            score +=1
        elif eg < 0:
            score -= 1
        if rr > 0.5:
            score +=1
        elif rr < 0.25:
            score -= 1

        if score >= 1:
            self.color = "#5FB538"
        elif score < -1:
            self.color = "#AE3D3D"
        else:
            self.color = "#FFD43C"

        self.var1.value.setText(f"{rg:.2%}")
        self.var2.value.setText(f"{eg:.2%}")
        self.var3.value.setText(f"{rr:.2%}")