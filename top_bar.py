from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import queries
from stylesheets import (
    search_box_css,
    minimize_css,
    maximize_css,
    close_css
)

class TopBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(50)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor("#E9E9E9")
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        self.setGraphicsEffect(shadow)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(50, 0, 10, 0)
        self.layout.setSpacing(0)

        self.search_box = StockPicker()
        self.search_box.setPlaceholderText("Search ...")
        self.search_box.setFixedWidth(300)
        self.search_box.setFixedHeight(40)
        self.search_box.setStyleSheet(search_box_css)
        self.layout.addWidget(self.search_box)

        self.path_label = QLabel("Equities  >  Stocks  >  International Business Machines Corp")
        self.path_label.setStyleSheet(
            """
            color: #8E8E8E;
            font-family: Lato;
            font-size: 14px;
            margin: 0px 0px 0px 10px
            """
        )
        self.path_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.path_label)

        self.path_label2 = QLabel(">  Overview")
        self.path_label2.setStyleSheet(
            """
            color: #000000;
            font-family: Lato;
            font-size: 14px;
            margin: 0px 0px 0px 5px
            """
        )
        self.path_label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.path_label2)

        self.placeholder = QFrame()
        self.layout.addWidget(self.placeholder)

        self.minimize_button = QPushButton()
        minimize_button_icon = QIcon("icons/minimize.svg")
        self.minimize_button.setIcon(minimize_button_icon)
        self.minimize_button.setIconSize(QSize(16, 16))
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setStyleSheet(minimize_css)
        self.layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton()
        maximize_button_icon = QIcon("icons/fullscreen.svg")
        self.maximize_button.setIcon(maximize_button_icon)
        self.maximize_button.setIconSize(QSize(14, 14))
        self.maximize_button.setFixedSize(40, 40)
        self.maximize_button.setStyleSheet(maximize_css)
        self.layout.addWidget(self.maximize_button)

        self.close_button = QPushButton()
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet(close_css)
        self.layout.addWidget(self.close_button)


class StockPicker(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = queries.get_stock_list()
        self.data = [" | ".join(t) for t in data]
        self.model = QStringListModel(self.data)
        self.completer = QCompleter()
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity(0))
        self.completer.setCompletionColumn(0)
        self.completer.setMaxVisibleItems(15)
        self.setCompleter(self.completer)
