from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page

class FactorsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)