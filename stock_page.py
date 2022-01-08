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