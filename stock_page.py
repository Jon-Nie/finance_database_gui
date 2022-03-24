from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import queries
from stylesheets import scrollarea_css
import sys


class StockPage(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)