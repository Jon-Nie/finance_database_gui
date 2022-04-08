from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from finance_database_gui.shared_widgets import *
from finance_database_gui.utils import equity_page_description

class EquitiesPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(20)

        self.header = SectionHeader(color="white", text="Equities")
        self.layout.addWidget(self.header, 0, 0)

        self.description = SectionDescription(
            color="white",
            text=equity_page_description
        )
        self.layout.addWidget(self.description, 1, 0)

        self.stocks_box = SectionCard(
            color="white",
            text="Stocks",
            description="Browse for stocks with the best fundamental conditions. See, how analysts and institutional money managers view the stock or find uncovered value stocks.",
            icon="stocks"
        )
        self.layout.addWidget(self.stocks_box, 1, 1)

        self.industries_box = SectionCard(
            color="white",
            text="Industries",
            description="Examine, how a company can be compared to its competitors and whether there are superior companies of the same industry.",
            icon="stocks"
        )
        self.layout.addWidget(self.industries_box, 1, 2)

        self.analysts_box = SectionCard(
            color="white",
            text="Institutionals",
            description="See, how big money managers performed in the past and what their portfolios look like.",
            icon="stocks"
        )
        self.layout.addWidget(self.analysts_box, 2, 0)

        self.institutionals_box = SectionCard(
            color="white",
            text="Analysts",
            description="Distinguish good and bad analysts and explore, what stocks they recommend and how accurate their recommendations were.",
            icon="stocks"
        )
        self.layout.addWidget(self.institutionals_box, 2, 1)

        self.factors_box = SectionCard(
            color="white",
            text="Factors",
            description="Explore academic variable-sorted portfolios, compute their factor exposure and find out, what works particularly well in the stock market.",
            icon="stocks"
        )
        self.layout.addWidget(self.factors_box, 2, 2)

        self.layout.addWidget(QFrame(), 3, 0)