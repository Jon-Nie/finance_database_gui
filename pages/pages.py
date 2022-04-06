from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .home_page import HomePage
from .equities_page import EquitiesPage
from .commodities_page import CommoditiesPage
from .economics_page import EconomicsPage
from .tracker_page import TrackerPage
from .backtests_page import BacktestsPage
from .stocks_page import StocksPage
from .stock_page import StockPage
from .industries_page import IndustriesPage
from .institutionals_page import InstitutionalsPage
from .institutional_page import InstitutionalPage
from .analysts_page import AnalystsPage
from .analyst_page import AnalystPage
from .factors_page import FactorsPage


class Pages(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent")

        self.home_page = HomePage()
        self.equities_page = EquitiesPage()
        self.commodities_page = CommoditiesPage()
        self.economics_page = EconomicsPage()
        self.tracker_page = TrackerPage()
        self.backtests_page = BacktestsPage()

        self.stocks_page = StocksPage()
        self.stock_page = StockPage()
        self.industries_page = IndustriesPage()
        self.institutionals_page = InstitutionalsPage()
        self.institutional_page = InstitutionalPage()
        self.analysts_page = AnalystsPage()
        self.analyst_page = AnalystPage()
        self.factors_page = FactorsPage()

        self.pages = (
            self.home_page,
            self.equities_page,
            self.commodities_page,
            self.economics_page,
            self.tracker_page,
            self.backtests_page,
            self.stocks_page,
            self.stock_page,
            self.industries_page,
            self.institutionals_page,
            self.institutional_page,
            self.analysts_page,
            self.analyst_page,
            self.factors_page
        )
        for page in self.pages:
            self.addWidget(page)