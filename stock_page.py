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


class ProfileBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = QFrame()
        self.layout.addWidget(self.content)
        self.content.layout = QHBoxLayout(self.content)

        self.left_side = QFrame()
        self.left_side.layout = QGridLayout(self.left_side)
        self.left_side.layout.setAlignment(Qt.AlignLeft)
        self.content.layout.addWidget(self.left_side)
        self.right_side = QFrame()
        self.right_side.layout = QVBoxLayout(self.right_side)
        self.content.layout.addWidget(self.right_side)

        self.country_flag = QLabel()
        self.country_flag.setFixedWidth(50)
        self.left_side.layout.addWidget(self.country_flag, 0, 0)

        self.country_name = QLabel()
        self.left_side.layout.addWidget(self.country_name, 0, 1)

        self.city = QLabel()
        self.left_side.layout.addWidget(self.city, 1, 0, 1, 1)

        self.street = QLabel()
        self.left_side.layout.addWidget(self.street, 2, 0, 1, 1)

        self.website = QLabel()
        self.left_side.layout.addWidget(self.website, 3, 0, 1, 1)

        self.employees = QLabel()
        self.left_side.layout.addWidget(self.employees, 4, 0, 1, 1)

        self.gics_header = QLabel("GICS")
        self.right_side.layout.addWidget(self.gics_header)

        self.gics_sector = QLabel()
        self.right_side.layout.addWidget(self.gics_sector)

        self.gics_industry = QLabel()
        self.right_side.layout.addWidget(self.gics_industry)

        self.sic_header = QLabel("SIC")
        self.right_side.layout.addWidget(self.sic_header)

        self.sic_division = QLabel()
        self.right_side.layout.addWidget(self.sic_division)

        self.sic_industry = QLabel()
        self.right_side.layout.addWidget(self.sic_industry)

    def update_data(self, profile):
        
        pixmap = QPixmap()
        pixmap.loadFromData(profile["country_flag"])
        pixmap = pixmap.scaledToWidth(50)
        self.country_flag.setPixmap(pixmap)

        self.country_name.setText(profile["country"])
        self.city.setText(f"{profile['zip']}, {profile['city']}")
        self.street.setText(profile["address1"])
        self.website.setText(profile["website"])
        self.employees.setText(f"{profile['employees']} Employees")

        self.gics_industry.setText(profile["gics_industry"])
        self.gics_sector.setText(profile["gics_sector"])
        self.sic_industry.setText(profile["sic_industry"])
        self.sic_division.setText(profile["sic_division"])


class KeyDataBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = QFrame()
        self.layout.addWidget(self.content)
        self.content.layout = QGridLayout(self.content)

        self.market_cap_label = QLabel("Market Cap")
        self.content.layout.addWidget(self.market_cap_label, 0, 0)

        self.revenue_label = QLabel("Revenue")
        self.content.layout.addWidget(self.revenue_label, 1, 0)

        self.income_label = QLabel("Net Income")
        self.content.layout.addWidget(self.income_label, 2, 0)

        self.revenue_growth_label = QLabel("Revenue Growth (3yr)")
        self.content.layout.addWidget(self.revenue_growth_label, 3, 0)

        self.income_growth_label = QLabel("Operating Income Growth (3yr)")
        self.content.layout.addWidget(self.income_growth_label, 4, 0)

        self.market_cap_value = QLabel()
        self.content.layout.addWidget(self.market_cap_value, 0, 1)

        self.revenue_value = QLabel()
        self.content.layout.addWidget(self.revenue_value, 1, 1)

        self.income_value = QLabel()
        self.content.layout.addWidget(self.income_value, 2, 1)

        self.revenue_growth_value = QLabel()
        self.content.layout.addWidget(self.revenue_growth_value, 3, 1)

        self.income_growth_value = QLabel()
        self.content.layout.addWidget(self.income_growth_value, 4, 1)        

        self.return_label = QLabel("1-Year Return")
        self.content.layout.addWidget(self.return_label, 0, 2)

        self.volatility_label = QLabel("1-Year Volatility")
        self.content.layout.addWidget(self.volatility_label, 1, 2)

        self.beta_label = QLabel("3-Year Beta")
        self.content.layout.addWidget(self.beta_label, 2, 2)

        self.pe_label = QLabel("P/E Ratio")
        self.content.layout.addWidget(self.pe_label, 3, 2)

        self.yield_label = QLabel("Dividend Yield")
        self.content.layout.addWidget(self.yield_label, 4, 2)

        self.return_value = QLabel()
        self.content.layout.addWidget(self.return_value, 0, 3)

        self.volatility_value = QLabel()
        self.content.layout.addWidget(self.volatility_value, 1, 3)

        self.beta_value = QLabel()
        self.content.layout.addWidget(self.beta_value, 2, 3)

        self.pe_value = QLabel()
        self.content.layout.addWidget(self.pe_value, 3, 3)

        self.yield_value = QLabel()
        self.content.layout.addWidget(self.yield_value, 4, 3)

    def update_data(self, time_series, fundamentals, currency):
        def conversion(number):
            if abs(number) > 1_000_000_000_000:
                number = number / 1_000_000_000_000
                unit = "T"
            elif abs(number) > 1_000_000_000:
                number = number / 1_000_000_000
                unit = "B"
            else :
                number = number / 1_000_000
                unit = "M"
            return (number, unit)
        market_cap, unit = conversion(time_series['market_cap'].iloc[-1])
        self.market_cap_value.setText(f"{market_cap:.2f}{unit} {currency}")

        revenue, unit = conversion(fundamentals['revenue ttm'].iloc[-1])
        self.revenue_value.setText(f"{revenue:.2f}{unit} {currency}")

        income, unit = conversion(fundamentals['net income ttm'].iloc[-1])
        self.income_value.setText(f"{income:.2f}{unit} {currency}")

        self.revenue_growth_value.setText(f"{(fundamentals['revenue ttm'].iloc[-1]/fundamentals['revenue ttm'].iloc[-13])**(1/4)-1:.2%}")
        self.income_growth_value.setText(f"{(fundamentals['operating income ttm'].iloc[-1]/fundamentals['operating income ttm'].iloc[-13])**(1/4)-1:.2%}")

        year_return = (((1+time_series["simple_return"]).cumprod() / (1+time_series["simple_return"]).cumprod().shift(250)) - 1).iloc[-1]
        self.return_value.setText(f"{year_return:.2%}")
        volatility = time_series["simple_return"][-250:].std() * np.sqrt(250)
        self.volatility_value.setText(f"{volatility:.2%}")
        pe = time_series["market_cap"].iloc[-1] / time_series["net income ttm"].iloc[-1].sum()
        self.pe_value.setText(f"{pe:.2f}")
        div_yield = time_series["dividends"][-250:].sum() / time_series["close"].iloc[-1]
        self.yield_value.setText(f"{div_yield:.2%}")


class DescriptionBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout.setSpacing(20)

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.description.setCursor(Qt.IBeamCursor)
        self.description.setAlignment(Qt.AlignJustify)
        self.description.setStyleSheet(
            """
            font-family: Lato;
            color: #444444;
            font-size: 14px;
            font-weight: normal;
            padding: 0px 0px 0px 0px;
            """
        )
        self.layout.addWidget(self.description)


class PriceChartBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_data(self, data):
        pass


class FundamentalSnapshotBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = QFrame()
        self.content.layout = QGridLayout(self.content)
        self.layout.addWidget(self.content)

        self.valuation_label = QLabel("Valuation")
        self.content.layout.addWidget(self.valuation_label, 0, 0)
        self.ey_value = QLabel()
        self.content.layout.addWidget(self.ey_value, 0, 1)
        self.ey_label = QLabel("Earnings Yield")
        self.content.layout.addWidget(self.ey_label, 1, 1)
        self.cfy_value = QLabel()
        self.content.layout.addWidget(self.cfy_value, 0, 2)
        self.cfy_label = QLabel("Cashflow Yield")
        self.content.layout.addWidget(self.cfy_label, 1, 2)
        self.ps_value = QLabel()
        self.content.layout.addWidget(self.ps_value, 0, 3)
        self.ps_label = QLabel("Price/Sales")
        self.content.layout.addWidget(self.ps_label, 1, 3)

        self.profitability_label = QLabel("Profitability")
        self.content.layout.addWidget(self.profitability_label, 2, 0)
        self.roa_value = QLabel()
        self.content.layout.addWidget(self.roa_value, 2, 1)
        self.roa_label = QLabel("Return on Assets")
        self.content.layout.addWidget(self.roa_label, 3, 1)
        self.roe_value = QLabel()
        self.content.layout.addWidget(self.roe_value, 2, 2)
        self.roe_label = QLabel("Return on Equity")
        self.content.layout.addWidget(self.roe_label, 3, 2)
        self.margin_value = QLabel()
        self.content.layout.addWidget(self.margin_value, 2, 3)
        self.margin_label = QLabel("Operating Margin")
        self.content.layout.addWidget(self.margin_label, 3, 3)

        self.growth_label = QLabel("Growth")
        self.content.layout.addWidget(self.growth_label, 4, 0)
        self.revenue_growth_value = QLabel()
        self.content.layout.addWidget(self.revenue_growth_value, 4, 1)
        self.revenue_growth_label = QLabel("Revenue Growth")
        self.content.layout.addWidget(self.revenue_growth_label, 5, 1)
        self.earnings_growth_value = QLabel()
        self.content.layout.addWidget(self.earnings_growth_value, 4, 2)
        self.earnings_growth_label = QLabel("Earnings Growth")
        self.content.layout.addWidget(self.earnings_growth_label, 5, 2)
        self.reinvestment_rate_value = QLabel()
        self.content.layout.addWidget(self.reinvestment_rate_value, 4, 3)
        self.reinvestment_rate_label = QLabel("Reinvestment Rate")
        self.content.layout.addWidget(self.reinvestment_rate_label, 5, 3)

        self.stability_label = QLabel("Stability")
        self.content.layout.addWidget(self.stability_label, 6, 0)
        self.equity_share_value = QLabel()
        self.content.layout.addWidget(self.equity_share_value, 6, 1)
        self.equity_share_label = QLabel("Equity Share")
        self.content.layout.addWidget(self.equity_share_label, 7, 1)
        self.debt_fcf_value = QLabel()
        self.content.layout.addWidget(self.debt_fcf_value, 6, 2)
        self.debt_fcf_label = QLabel("Net Debt/FCF")
        self.content.layout.addWidget(self.debt_fcf_label, 7, 2)
        self.coverage_value = QLabel()
        self.content.layout.addWidget(self.coverage_value, 6, 3)
        self.coverage_label = QLabel("Interest Coverage")
        self.content.layout.addWidget(self.coverage_label, 7, 3)


    def update_data(self, fundamentals):
        self.ey_value.setText(f"{1/fundamentals['p/e'][-1]:.2%}")
        self.cfy_value.setText(f"{1/fundamentals['p/cf'][-1]:.2%}")
        self.ps_value.setText(f"{fundamentals['p/s'][-1]:.2f}")

        self.roa_value.setText(f"{fundamentals['roa ttm'][-1]:.2%}")
        self.roe_value.setText(f"{fundamentals['roe ttm'][-1]:.2%}")
        self.margin_value.setText(f"{fundamentals['net margin ttm'][-1]:.2%}")

        self.revenue_growth_value.setText(f"{fundamentals['revenue growth ttm'][-1]:.2%}")
        self.earnings_growth_value.setText(f"{fundamentals['net income growth ttm'][-1]:.2%}")
        self.reinvestment_rate_value.setText(f"{fundamentals['reinvestment rate ttm'][-1]:.2%}")

        self.equity_share_value.setText(f"{fundamentals['equity share ttm'][-1]:.2%}")
        self.debt_fcf_value.setText(f"{fundamentals['debt/fcf ttm'][-1]:.2f}")
        self.coverage_value.setText(f"{fundamentals['interest coverage ttm'][-1]:.2f}")


class NewsBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout.addWidget(QFrame())
    
    def update_data(self, data):
        pass


class ExecutivesBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_data(self, data):
        pass


class CompetitorsBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_data(self, data):
        pass


class AnalystRecommendationsBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_data(self, data):
        pass


class RecommendationTrendBox(BoxTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_data(self, data):
        pass


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