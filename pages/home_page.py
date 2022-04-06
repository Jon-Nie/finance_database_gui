from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from finance_database_gui.shared_widgets import *
from finance_database_gui.utils import home_page_description

class HomePage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(20)

        self.header = SectionHeader(color="blue", text="Finance Database GUI")
        self.layout.addWidget(self.header, 0, 0)

        self.description = SectionDescription(
            color="blue",
            text=home_page_description
        )
        self.layout.addWidget(self.description, 1, 0)

        self.equities_box = SectionCard(
            color="blue",
            text="Equities",
            description="Compare different ETFs with each other, develop a good grasp of a stocks' outlook and build efficient portfolios.",
            icon="stocks"
        )
        self.layout.addWidget(self.equities_box, 1, 1)

        self.commodities_box = SectionCard(
            color="blue",
            text="Commodities",
            description="Examine, how different commodities performed in the past, how their returns could be explained and pick the commodities with the highest premia.",
            icon="stocks"
        )
        self.layout.addWidget(self.commodities_box, 1, 2)

        self.economics_box = SectionCard(
            color="blue",
            text="Economics",
            description="Explore a rich dataset of macroeconomic variables and build your investment thesis upon it.",
            icon="stocks"
        )
        self.layout.addWidget(self.economics_box, 2, 0)

        self.tracker_box = SectionCard(
            color="blue",
            text="Portfolio Tracker",
            description="See, how your portfolio performed compared to a benchmark and examine its factor exposure.",
            icon="stocks"
        )
        self.layout.addWidget(self.tracker_box, 2, 1)

        self.backtests_box = SectionCard(
            color="blue",
            text="Backtests",
            description="Backtest your strategies with an easy-to-use frontend that lets you pick variables, timeframes etc. and returns a comprehensive overview of investment strategies.",
            icon="stocks"
        )
        self.layout.addWidget(self.backtests_box, 2, 2)

        self.layout.addWidget(QFrame(), 3, 0)

    def background(self):
        return """
            QFrame {
                background-color: #3E75C8
            }
        """