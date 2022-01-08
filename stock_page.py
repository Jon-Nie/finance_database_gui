from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from base_classes import Page
import numpy as np
import queries


class StockPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)

        self.content = QFrame()
        self.content.layout = QVBoxLayout(self.content)
        self.content.layout.setContentsMargins(30, 0, 0, 50)
        self.content.layout.setSpacing(20)

        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.horizontalScrollBar().setFixedHeight(7)
        self.scrollarea.verticalScrollBar().setFixedWidth(7)
        self.scrollarea.setStyleSheet(
            """
            QScrollArea {
                border: None
            }
            QScrollBar:handle {
                border: None;
                background-color: #d4d4d4;
                border-radius: 3px;
            }
            QScrollBar:handle:hover {
                background-color: #ababab;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #F6F8FB;
            }
            """
        )
        self.scrollarea.setWidget(self.content)

        self.header_section = HeaderSection()
        self.content.layout.addWidget(self.header_section)
        self.separator = QFrame()
        self.separator.setFixedHeight(1)
        self.separator.setStyleSheet("background-color: #C4C4C4; margin: 10px")
        self.content.layout.addWidget(self.separator)
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

        self.layout.addWidget(self.scrollarea)

        self.orientation_bar = OrientationBar()
        self.layout.addWidget(self.orientation_bar)
    
    def update_data(self, ticker):
        data = queries.get_stock_data(ticker)
        self.header_section.update_data(data)
        self.overview_section.update_data(data)


class OrientationBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(200)


class BoxTemplate(QFrame):
    def __init__(self, header_label, icon_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: None;
                border-radius: 5px;
            }
            """
        )

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow_color = QColor("#999999")
        self.shadow_color.setAlpha(80)
        self.shadow.setColor(self.shadow_color)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 20, 40, 30)

        self.header = BoxHeader(header_label, icon_path)
        self.layout.addWidget(self.header)


class BoxHeader(QLabel):
    def __init__(self, text, icon_path, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.setAlignment(Qt.AlignLeft)
        self.setMaximumHeight(40)
        self.setStyleSheet(
            """
            font-family: Lato;
            font-weight: Bold;
            font-size: 20px;
            """
        )

        self.icon_path = icon_path


class HeaderSection(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("HeaderSection")

        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(20)
        self.layout.setAlignment(Qt.AlignLeft)

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
        self.layout.addWidget(self.name, 0, 2, 1, 3)

        self.ticker = QLabel()
        self.ticker.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-weight: Bold;
                font-size: 20px;
            }
            """
        )
        self.layout.addWidget(self.ticker, 1, 2)

        self.isin = QLabel()
        self.isin.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-weight: Bold;
                font-size: 20px;
            }
            """
        )
        self.layout.addWidget(self.isin, 1, 3)

        self.price = QLabel()
        self.price.setStyleSheet(
            """
            QLabel {
                font-family: Lato;
                font-weight: Bold;
                font-size: 20px;
            }
            """
        )
        self.layout.addWidget(self.price, 1, 4)

        self.layout.addWidget(QFrame(), 1, 5)
    
    def update_data(self, data):
        profile = data["profile"]
        pixmap = QPixmap()
        pixmap.loadFromData(profile["logo"])
        pixmap = pixmap.scaledToWidth(100)
        self.logo.setPixmap(pixmap)

        self.name.setText(profile["name"])
        self.ticker.setText(profile["ticker"])
        self.isin.setText(profile["isin"])
        self.price.setText(f"{data['time_series']['close'].iloc[-1]:.2f} {profile['currency']}")


class OverviewSection(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("OverviewSection")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setHorizontalSpacing(15)
        self.layout.setVerticalSpacing(25)

        self.profile_box = ProfileBox("Profile", None)
        self.layout.addWidget(self.profile_box, 0, 0)

        self.key_data_box = KeyDataBox("Key Data", None)
        self.layout.addWidget(self.key_data_box, 0, 1)

        self.description_box = DescriptionBox("Business Description", None)
        self.layout.addWidget(self.description_box, 1, 0, 1, 2)

        self.chart_box = PriceChartBox("Price Chart", None)
        self.layout.addWidget(self.chart_box, 2, 0)

        self.snapshot_box = FundamentalSnapshotBox("Fundamental Snapshot", None)
        self.layout.addWidget(self.snapshot_box, 3, 0)

        self.news_box = NewsBox("News", None)
        self.layout.addWidget(self.news_box, 2, 1, 2, 1)

    def update_data(self, data):
        self.profile_box.update_data(data["profile"])
        self.key_data_box.update_data(data["time_series"], data["fundamentals"], data["profile"]["currency"])
        self.description_box.description.setText(data["profile"]["description"])
        self.chart_box.update_data(data["time_series"])
        self.snapshot_box.update_data(data["time_series"])
        self.news_box.update_data(data["news"])


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