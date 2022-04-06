from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from stylesheets import app_css

class Page(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def background(self):
        return app_css