from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .page import Page

class HomePage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def background(self):
        return """
            QFrame {
                background-color: #3E75C8
            }
        """