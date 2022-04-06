from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page
from finance_database_gui.shared_widgets import ContentBox

class StocksPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)