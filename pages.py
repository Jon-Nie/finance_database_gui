from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from home_page import HomePage
from equities_page import EquitiesPage
from stock_page import StockPage
from commodities_page import CommoditiesPage
from economics_page import EconomicDataPage
from tracker_page import PortfolioTrackerPage
from backtests_page import BacktestsPage

class Pages(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.home_page = HomePage()
        self.equities_page = EquitiesPage()
        self.stock_page = StockPage()
        self.commodities_page = CommoditiesPage()
        self.economics_page = EconomicDataPage()
        self.tracker_page = PortfolioTrackerPage()
        self.backtests_page = BacktestsPage()

        self.pages = (
            self.home_page,
            self.equities_page,
            self.stock_page,
            self.commodities_page,
            self.economics_page,
            self.tracker_page,
            self.backtests_page
        )
        for page in self.pages:
            self.addWidget(page)