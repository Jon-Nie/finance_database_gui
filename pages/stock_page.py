from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCharts import QtCharts
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from .page import Page
from shared_widgets import Label, ContentBox
from finance_database_gui.stylesheets import chart_option_button_css

class StockPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(20)

        self.upper_layout = QGridLayout()
        self.upper_layout.setSpacing(20)
        self.layout.addLayout(self.upper_layout)
        self.lower_layout = QHBoxLayout()
        self.lower_layout.setSpacing(20)
        self.layout.addLayout(self.lower_layout)

        self.characteristics_box = CharacteristicsBox()
        self.upper_layout.addWidget(self.characteristics_box, 0, 0, 1, 1)

        self.news_box = NewsBox()
        self.upper_layout.addWidget(self.news_box, 0, 1, 2, 1)

        self.description_box = DescriptionBox()
        self.upper_layout.addWidget(self.description_box, 1, 0, 1, 1)

        self.prices_box = PriceBox()
        self.upper_layout.addWidget(self.prices_box, 0, 2, 2, 1)

        self.analysts_box = AnalystsBox()
        self.lower_layout.addWidget(self.analysts_box)

        self.value_box = ValueBox("Value", "Earnings Yield", "Price-to-Book", "Price-to-Sales")
        self.lower_layout.addWidget(self.value_box)

        self.profitability_box = ProfitabilityBox("Profitability", "Return on Equity", "Return on Assets", "Net Margin")
        self.lower_layout.addWidget(self.profitability_box)

        self.growth_box = GrowthBox("Growth (3yr)", "Revenue Growth", "Earnings Growth", "Reinvestment Rate")
        self.lower_layout.addWidget(self.growth_box)

        self.fundamental_view = FundamentalView()
        self.lower_layout.addWidget(self.fundamental_view)


class CharacteristicsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumHeight(120)

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

        self.placeholder = QFrame()
        self.layout.addWidget(self.update_button, 0, 9, 2, 1)


class Logo(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QPixmap()
        self.setStyleSheet("Qlabel {margin-right:10px}")

    @Slot(bytes)
    def update_logo(self, logo):
        self.icon.loadFromData(logo)
        if self.icon.width() > self.icon.height():
            self.icon = self.icon.scaledToWidth(80, Qt.SmoothTransformation)
        else:
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


class DescriptionBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(750, 300)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(10)

        self.address = DescriptionAddress()
        self.layout.addWidget(self.address)

        self.industry = DescriptionIndustry()
        self.layout.addWidget(self.industry)

        self.separator = QFrame()
        self.separator.setMinimumHeight(1)
        self.separator.setStyleSheet(
            """
            QFrame {
                background-color: #BCBCBC;
                margin-right: 10px;
            }
            """
        )
        self.layout.addWidget(self.separator)

        self.description = BusinessDescription()
        self.layout.addWidget(self.description)


class BusinessDescription(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setSingleStep(5)

        self.description = Label()
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignJustify)
        self.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 13px;
                font-weight: 600;
                color: #333333;
                padding-right: 10px
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

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setVerticalSpacing(0)
        self.layout.setHorizontalSpacing(10)

        self.header = Label("Description")
        self.header.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 20px;
                font-weight: 600;
                color: #333333
            }
            """
        )
        self.header.setMinimumWidth(200)
        self.layout.addWidget(self.header, 0, 0, 1, 2)

        self.country_logo = CountryLogo()
        self.layout.addWidget(self.country_logo, 0, 1, 1, 1)

        self.country_name = Label()
        self.layout.addWidget(self.country_name, 1, 1, 1, 1)
        
        self.city = Label()
        self.layout.addWidget(self.city, 0, 2, 1, 1)

        self.street = Label()
        self.layout.addWidget(self.street, 1, 2, 1, 1)

        self.website = Label()
        self.layout.addWidget(self.website, 0, 3, 1, 1)

        self.employees = Label()
        self.layout.addWidget(self.employees, 1, 3, 1, 1)

        self.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 13px;
                font-weight: 500;
                color: #333333
            }
            """
        )

class CountryLogo(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QPixmap()

        self.setStyleSheet(
            """
            QPushButton {
                font-family: Lato;
                font-size: 13px;
                font-weight: 500;
                color: #333333;
                text-align: left
            }
            """
        )

    @Slot(bytes)
    def update_icon(self, logo):
        self.icon.loadFromData(logo)
        self.icon = self.icon.scaledToHeight(15, Qt.SmoothTransformation)
        self.setPixmap(self.icon)


class DescriptionIndustry(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setVerticalSpacing(5)
        self.layout.setHorizontalSpacing(10)

        self.gics = Label("GICS")
        self.gics.setObjectName("header")
        self.layout.addWidget(self.gics, 0, 0, 1, 1)

        self.gics_sector = Label()
        self.gics_sector.setObjectName("value")
        self.layout.addWidget(self.gics_sector, 0, 1, 1, 1)

        self.gics_industry = Label()
        self.gics_industry.setObjectName("value")
        self.gics_industry.setMinimumWidth(400)
        self.layout.addWidget(self.gics_industry, 0, 2, 1, 1)

        self.sic = Label("SIC")
        self.sic.setObjectName("header")
        self.layout.addWidget(self.sic, 1, 0, 1, 1)

        self.sic_division = Label()
        self.sic_division.setObjectName("value")
        self.layout.addWidget(self.sic_division, 1, 1, 1, 1)

        self.sic_industry = Label()
        self.sic_industry.setMinimumWidth(400)
        self.sic_industry.setObjectName("value")
        self.sic_industry.setWordWrap(True)
        self.layout.addWidget(self.sic_industry, 1, 2, 1, 1)

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
                font-size: 13px;
                font-weight: 500;
                color: #333333
            }
            """
        )

        self.placeholder = QFrame()
        self.placeholder.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.layout.addWidget(self.placeholder, 0, 3, 2, 1)


class DescriptionExcutives(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NewsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(200)

        self.news = []

        self.layout = QHBoxLayout(self)


class PriceBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(370)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.price_view = PriceView()
        self.layout.addWidget(self.price_view)

        self.descriptive_statistics = DescriptiveStatistics()
        self.layout.addWidget(self.descriptive_statistics)


class PriceView(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(200)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #3E75C8
            }
            """
        )

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 0)
        self.layout.setSpacing(0)

        self.timeframe_picker = TimeFramePicker()
        for button in self.timeframe_picker.buttons.values():
            button.clicked.connect(self.update_data)
        self.timeframe_picker.options_button.clicked.connect(self.show_options)
        self.layout.addWidget(self.timeframe_picker)

        self.chartview = QtCharts.QChartView()
        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.chartview)

        self.options_frame = OptionsFrame(self)
        self.options_frame.hide()

        self.options_frame.log.stateChanged.connect(self.update_data)
        self.options_frame.adjusted.stateChanged.connect(self.update_data)
        self.options_frame.raw.stateChanged.connect(self.update_data)
    
    @Slot(pd.Series)
    def set_data(self, series):
        self.data = series.dropna()
        self.update_data()
    
    def show_options(self):
        self.options_frame.setGeometry(self.width()-230, 70, 230, 130)
        if self.options_frame.isHidden():
            self.options_frame.show()
        else:
            self.options_frame.hide()

    
    def update_data(self):
        if self.sender() in self.timeframe_picker.buttons.values():
            label = self.sender().text()
        elif self.sender() in (self.options_frame.log, self.options_frame.adjusted, self.options_frame.raw):
            for button in self.timeframe_picker.buttons.values():
                if button.objectName() == "active":
                    label = button.text()
        else:
            label = "1Yr"
        for text, button in self.timeframe_picker.buttons.items():
            if text == label:
                button.setObjectName("active")
            else:
                button.setObjectName("inactive")
            button.setStyleSheet(chart_option_button_css)

        if "Yr" in label:
            ts = (pd.to_datetime("today") - relativedelta(years=self.timeframe_picker.deltas[label])).timestamp()
        elif label != "Max":
            ts = (pd.to_datetime("today") - relativedelta(months=self.timeframe_picker.deltas[label])).timestamp()
        else:
            ts = pd.to_datetime("1900-01-01").timestamp()

        self.series = QtCharts.QLineSeries()
        pen = QPen()
        pen.setWidth(2)
        pen.setColor("#FFFFFF")
        self.series.setPen(pen)
        for index in self.data.loc[ts:].index:
            if self.options_frame.log.isChecked():
                self.series.append(index, np.log(self.data.loc[index]))
            else:

                self.series.append(index, self.data.loc[index])

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.series)
        self.chart.setBackgroundBrush(QBrush(QColor("transparent")))
        self.chart.legend().hide()
        self.chartview.setChart(self.chart)


class OptionsFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: #497ECD")

        self.layout = QVBoxLayout(self)

        self.header = QLabel("Options")
        self.header.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 14px;
                font-weight: 600;
                color: #FFFFFF
            }
            """
        )
        self.layout.addWidget(self.header)

        self.log = QCheckBox("Logarithmized Prices")
        self.log.setStyleSheet(
            """
            QCheckBox {
                font-family: Lato;
                font-size: 12px;
                font-weight: 600;
                color: #FFFFFF
            }
            """
        )
        self.layout.addWidget(self.log)

        self.adjusted = QCheckBox("Include Dividends/Adjusted Close")
        self.adjusted.setStyleSheet(
            """
            QCheckBox {
                font-family: Lato;
                font-size: 12px;
                font-weight: 600;
                color: #FFFFFF
            }
            """
        )
        self.layout.addWidget(self.adjusted)

        self.raw = QCheckBox("Raw Prices / Ignore Splits")
        self.raw.setStyleSheet(
            """
            QCheckBox {
                font-family: Lato;
                font-size: 12px;
                font-weight: 600;
                color: #FFFFFF
            }
            """
        )
        self.layout.addWidget(self.raw)


class TimeFramePicker(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(30)
        self.setStyleSheet(chart_option_button_css)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.buttons = {}
        self.deltas = {
            "1M": 1,
            "3M": 3,
            "6M": 6,
            "1Yr": 1,
            "5Yr": 5,
            "10Yr": 10,
            "25Yr": 25
        }
        for label in (
            "1M",
            "3M",
            "6M",
            "1Yr",
            "5Yr",
            "10Yr",
            "25Yr",
            "Max"
        ):
            button = QPushButton(label)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.setFixedSize(35, self.height())
            self.layout.addWidget(button)
            self.buttons[label] = button

        self.options_button = OptionsButton()
        self.options_button.setFixedHeight(self.height())
        self.layout.addWidget(self.options_button)


class OptionsButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
            }
            """
        )
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#FFFFFF"))

        width, height = (4, 4)
        painter.drawEllipse(QRectF(self.width()/2-width/2, self.height()/5, width, height))
        painter.drawEllipse(QRectF(self.width()/2-width/2, self.height()*2/5, width, height))
        painter.drawEllipse(QRectF(self.width()/2-width/2, self.height()*3/5, width, height))

        painter.end()


class DescriptiveStatistics(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AnalystsBox(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(220)
        self.setFixedWidth(200)

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
                font-size: 13px;
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
        self.setFixedHeight(220)
        self.setFixedWidth(160)
        self.color = "black"

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.placeholder = QFrame()
        self.placeholder.setStyleSheet("background-color: transparent")
        self.placeholder.setMinimumHeight(20)
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
        self.placeholder2.setMinimumHeight(10)
        self.layout.addWidget(self.placeholder2)

        self.var1 = FactorBoxItem(var1)
        self.layout.addWidget(self.var1)

        self.var2 = FactorBoxItem(var2)
        self.layout.addWidget(self.var2)

        self.var3 = FactorBoxItem(var3)
        self.layout.addWidget(self.var3)

        self.placeholder3 = QFrame()
        self.placeholder3.setMinimumHeight(10)
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
    
    @Slot(pd.DataFrame)
    def set_data(self, data):
        self.data = data
        self.update_data()

    def update_data(self):
        score = 0
        ey = self.data.loc[self.data.index[-1], "e/p"]
        bm = self.data.loc[self.data.index[-1], "b/m"]
        sp = self.data.loc[self.data.index[-1], "s/p"]
        if ey > 0.05:
            score +=1
        elif ey < 0.3:
            score -= 1
        if bm > 0.5:
            score +=1
        elif bm < 0.1:
            score -= 1
        if sp > 1:
            score +=1
        elif sp < 0.2:
            score -= 1

        if score >= 1:
            self.color = "#5FB538"
        elif score < -1:
            self.color = "#AE3D3D"
        else:
            self.color = "#FFD43C"
        
        self.var1.value.setText(f"{ey:.2%}")
        self.var2.value.setText(f"{1/bm:.2f}")
        self.var3.value.setText(f"{1/sp:.2f}")


class ProfitabilityBox(FactorBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Slot(pd.DataFrame)
    def set_data(self, data):
        self.data = data
        self.update_data()

    def update_data(self):
        score = 0
        roe = self.data.loc[self.data.index[-1], "roe ttm"]
        roa = self.data.loc[self.data.index[-1], "roa ttm"]
        margin = self.data.loc[self.data.index[-1], "net margin ttm"]
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

    def set_data(self, data):
        self.data = data
        self.update_data()

    @Slot(pd.DataFrame)
    def update_data(self):
        score = 0
        rg = self.data.loc[self.data.index[-1], "revenue growth ttm"]
        eg = self.data.loc[self.data.index[-1], "net income growth ttm"]
        rr = self.data.loc[self.data.index[-1], "reinvestment rate ttm"]
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

class FundamentalView(ContentBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(220)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header = Label()
        self.header.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-size: 20px;
                font-weight: 600;
                color: #333333;
                padding: 20px 0px 0px 40px
            }
            """
        )
        self.layout.addWidget(self.header)

        self.chartview = QtCharts.QChartView()
        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.chartview)

    @Slot(pd.Series, str)
    def set_data(self, data, name):
        self.data = data.dropna()
        self.update_data()
        self.header.setText(name)
    
    def update_data(self):
        self.barset = QtCharts.QBarSet("")
        self.barset.setColor("#3E75C8")
        self.barset.append(list(self.data.values))

        self.series = QtCharts.QBarSeries()
        self.series.append(self.barset)

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.series)
        self.chartview.setChart(self.chart)
        self.chart.legend().hide()