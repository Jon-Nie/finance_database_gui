import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from top_bar import *
from sidebar import *
from top_bar import *
from pages.pages import Pages
from stylesheets import (
    app_css,
    grip_css,
    button_frame_css
)
from models import StockData

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(175, 50, 1600, 900)
        self.setWindowFlags(Qt.Window.FramelessWindowHint)
        
        self.central = QWidget(self)
        self.central.setStyleSheet(app_css)
        self.setCentralWidget(self.central)

        self.layout = QHBoxLayout(self.central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.sidebar = SideBar()
        self.layout.addWidget(self.sidebar)

        self.content = Content()
        self.layout.addWidget(self.content)

        self.content.topbar.minimize_button.clicked.connect(self.showMinimized)
        self.content.topbar.maximize_button.clicked.connect(self.maximize_restore)
        self.content.topbar.close_button.clicked.connect(self.close)

        self.content.topbar.mouseMoveEvent = self.moveWindow

        self.size_grip_left = QFrame(self)
        self.size_grip_left.setStyleSheet(grip_css)
        self.size_grip_left.setCursor(Qt.SizeHorCursor)
        self.size_grip_left.installEventFilter(self)

        self.size_grip_top = QFrame(self)
        self.size_grip_top.setStyleSheet(grip_css)
        self.size_grip_top.setCursor(Qt.SizeVerCursor)
        self.size_grip_top.installEventFilter(self)

        self.size_grip_right = QFrame(self)
        self.size_grip_right.setStyleSheet(grip_css)
        self.size_grip_right.setCursor(Qt.SizeHorCursor)
        self.size_grip_right.installEventFilter(self)

        self.size_grip_bottom = QFrame(self)
        self.size_grip_bottom.setStyleSheet(grip_css)
        self.size_grip_bottom.setCursor(Qt.SizeVerCursor)
        self.size_grip_bottom.installEventFilter(self)

        self.size_grip_top_left = QSizeGrip(self)
        self.size_grip_top_left.setStyleSheet(grip_css)

        self.size_grip_top_right = QSizeGrip(self)
        self.size_grip_top_right.setStyleSheet(grip_css)

        self.size_grip_bottom_right = QSizeGrip(self)
        self.size_grip_bottom_right.setStyleSheet(grip_css)

        self.size_grip_bottom_left = QSizeGrip(self)
        self.size_grip_bottom_left.setStyleSheet(grip_css)

        for button in self.button_page_match:
            button.clicked.connect(self.button_to_page_clicked)

        self.content.topbar.search_box.returnPressed.connect(self.searchbox_clicked)
        
        self.model = StockData()
        self.set_connections(self.model)
    
    def paintEvent(self, event):
        width, height = 5, 5

        self.size_grip_left.setGeometry(0, 0, width, self.height())
        self.size_grip_top.setGeometry(0, 0, self.width(), height)
        self.size_grip_right.setGeometry(self.width() - width, 0, width, self.height())
        self.size_grip_bottom.setGeometry(0, self.height() - height, self.width(), height)
        
        self.size_grip_top_left.setGeometry(0, 0, width, height)
        self.size_grip_top_right.setGeometry(self.width() - width, 0, width, height)
        self.size_grip_bottom_right.setGeometry(self.width() - width, self.height() - height, width, height)
        self.size_grip_bottom_left.setGeometry(0, self.height() - height, width, height)
    
    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseMove:
            mouse_position = event.globalPos()
            width = self.geometry().width()
            height = self.geometry().height()
            if object == self.size_grip_left:
                self.setGeometry(mouse_position.x(), self.geometry().y(), self.geometry().x() + width - mouse_position.x(), height)
            if object == self.size_grip_top:
                self.setGeometry(self.geometry().x(), mouse_position.y(), width, self.geometry().y() + height - mouse_position.y())
            if object == self.size_grip_right:
                self.setGeometry(self.geometry().x(), self.geometry().y(), mouse_position.x() - self.geometry().x(), height)
            if object == self.size_grip_bottom:
                self.setGeometry(self.geometry().x(), self.geometry().y(), width, mouse_position.y() - self.geometry().y())
            return True
        return super().eventFilter(object, event)

    def moveWindow(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    @property
    def button_page_match(self):
        dct = {
            self.sidebar.button_frame.home_button: self.content.pages.home_page,
            self.sidebar.button_frame.equities_button: self.content.pages.equities_page,
            self.sidebar.button_frame.commodities_button: self.content.pages.commodities_page,
            self.sidebar.button_frame.economics_button: self.content.pages.economics_page,
            self.sidebar.button_frame.tracker_button: self.content.pages.tracker_page,
            self.sidebar.button_frame.backtests_button: self.content.pages.backtests_page,

            self.content.pages.home_page.equities_box.button: self.content.pages.equities_page,
            self.content.pages.home_page.commodities_box.button: self.content.pages.commodities_page,
            self.content.pages.home_page.economics_box.button: self.content.pages.economics_page,
            self.content.pages.home_page.tracker_box.button: self.content.pages.tracker_page,
            self.content.pages.home_page.backtests_box.button: self.content.pages.backtests_page,
            self.content.pages.equities_page.stocks_box.button: self.content.pages.stocks_page,
            self.content.pages.equities_page.industries_box.button: self.content.pages.industries_page,
            self.content.pages.equities_page.institutionals_box.button: self.content.pages.institutionals_page,
            self.content.pages.equities_page.analysts_box.button: self.content.pages.analysts_page,
            self.content.pages.equities_page.factors_box.button: self.content.pages.factors_page,
        }
        return dct
    
    @property
    def page_sidebar_match(self):
        dct = {
            self.content.pages.home_page: self.sidebar.button_frame.home_button,
            self.content.pages.equities_page: self.sidebar.button_frame.equities_button,
            self.content.pages.commodities_page: self.sidebar.button_frame.commodities_button,
            self.content.pages.economics_page: self.sidebar.button_frame.economics_button,
            self.content.pages.tracker_page: self.sidebar.button_frame.tracker_button,
            self.content.pages.backtests_page: self.sidebar.button_frame.backtests_button,

            self.content.pages.equities_page: self.sidebar.button_frame.equities_button,
            self.content.pages.commodities_page: self.sidebar.button_frame.commodities_button,
            self.content.pages.economics_page: self.sidebar.button_frame.economics_button,
            self.content.pages.tracker_page: self.sidebar.button_frame.tracker_button,
            self.content.pages.backtests_page: self.sidebar.button_frame.backtests_button,
            self.content.pages.stocks_page: self.sidebar.button_frame.equities_button,
            self.content.pages.industries_page: self.sidebar.button_frame.equities_button,
            self.content.pages.institutionals_page: self.sidebar.button_frame.equities_button,
            self.content.pages.analysts_page: self.sidebar.button_frame.equities_button,
            self.content.pages.factors_page: self.sidebar.button_frame.equities_button,
        }
        return dct
    
    def searchbox_clicked(self):
        ticker, name, type_ = self.content.topbar.search_box.text().split("   ")
        ticker, name, type_ = ticker.strip(), name.strip(), type_.strip()
        if type_ == "Stock":
            self.content.setCurrentWidget(self.content.pages.stock_page)
            self.model.setData(self.model.index(-1, -1, QModelIndex()), ticker)

            self.sidebar.button_frame.change_stylesheet(self.sidebar.button_frame.equities_button)
            self.sidebar.button_frame.setObjectName("white")
            self.sidebar.button_frame.setStyleSheet(button_frame_css)
        self.content.topbar.search_box.clear()
    
    def button_to_page_clicked(self):
        page = self.button_page_match[self.sender()]
        self.content.setCurrentWidget(page)
        if page == self.content.pages.home_page:
            self.sidebar.button_frame.setObjectName("blue")
        else:
            self.sidebar.button_frame.setObjectName("white")
        self.sidebar.button_frame.setStyleSheet(button_frame_css)

        self.sidebar.button_frame.change_stylesheet(self.page_sidebar_match[self.button_page_match[self.sender()]])

    def set_connections(self, model):
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(model)
        self.mapper.setOrientation(Qt.Vertical)
        self.model.update_logo.connect(self.content.pages.stock_page.characteristics_box.logo.update_logo)
        self.mapper.addMapping(self.content.pages.stock_page.characteristics_box.name, 1, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.characteristics_box.ticker.value, 2, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.characteristics_box.isin.value, 3, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.characteristics_box.last_price.value, 4, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.characteristics_box.market_cap.value, 5, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.characteristics_box.pe_ratio.value, 6, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.characteristics_box.payout_yield.value, 7, b"text")
        self.model.update_country_icon.connect(self.content.pages.stock_page.description_box.address.country.update_icon)
        self.mapper.addMapping(self.content.pages.stock_page.description_box.address.country, 9, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.address.city, 10, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.address.street, 11, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.address.website, 12, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.address.employees, 13, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.industry.gics_sector, 14, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.industry.gics_industry, 15, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.industry.sic_division, 16, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.industry.sic_industry, 17, b"text")
        self.mapper.addMapping(self.content.pages.stock_page.description_box.description.description, 18, b"text")
        self.model.update_value.connect(self.content.pages.stock_page.value_box.update_data)
        self.model.update_profitability.connect(self.content.pages.stock_page.profitability_box.update_data)
        self.model.update_growth.connect(self.content.pages.stock_page.growth_box.update_data)
        self.mapper.toFirst()


class Content(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.topbar = TopBar()
        self.layout.addWidget(self.topbar)

        self.pages = Pages()
        self.layout.addWidget(self.pages)

    def setCurrentWidget(self, page):
        self.pages.setCurrentWidget(page)
        self.setStyleSheet(page.background())
        if page == self.pages.home_page:
            self.topbar.change_style("blue")
        else:
            self.topbar.change_style("white")


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    window.show()
    sys.exit(app.exec_())