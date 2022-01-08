from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import queries

class TopBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #F6F8FB")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(50, 0, 0, 0)
        self.layout.setSpacing(0)

        self.search_box = StockPicker()
        self.search_box.setPlaceholderText("Search ...")
        self.search_box.setFixedWidth(300)
        self.search_box.setFixedHeight(40)
        self.search_box.setStyleSheet(
            """
            font-family: Lato;
            font-size: 14px;
            background-color: #FFFFFF;
            color: black;
            border-radius: 15px;
            border: 1px solid #a8a8a8;
            padding: 0px 10px 0px 10px;
            margin: 10px 0px 0px 0px
            """
        )
        self.layout.addWidget(self.search_box)

        self.path_label = QLabel("Equities  >  Stocks  >  International Business Machines Corp")
        self.path_label.setStyleSheet(
            """
            color: #8E8E8E;
            font-family: Lato;
            font-size: 14px;
            margin: 10px 0px 0px 10px
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
            margin: 10px 0px 0px 5px
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
        self.minimize_button.setStyleSheet(
            """
            QPushButton {
                border: None;
                padding: 15px 10px 10px 10px;
            }
            QPushButton:hover {
                background-color: #dcdfe3;
            }
            """
        )
        self.layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton()
        maximize_button_icon = QIcon("icons/maximize.svg")
        self.maximize_button.setIcon(maximize_button_icon)
        self.maximize_button.setIconSize(QSize(14, 14))
        self.maximize_button.setFixedSize(40, 40)
        self.maximize_button.setStyleSheet(
            """
            QPushButton {
                border: None;
                padding: 12.5px;
            }
            QPushButton:hover {
                background-color: #dcdfe3;
            }
            QPushButton:hover:pressed {
                background-color: #babcbf;
            }
            """
        )
        self.layout.addWidget(self.maximize_button)

        self.close_button = QPushButton()
        close_button_icon = QIcon("icons/close.svg")
        self.close_button.setIcon(close_button_icon)
        self.close_button.setIconSize(QSize(20, 20))
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet(
            """
            QPushButton {
                border: None;
                padding:10px
            }
            QPushButton:hover {
                background-color: #ed3b3b;
            }
            QPushButton:hover:pressed {
                background-color: #a32222
            }
            """
        )
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