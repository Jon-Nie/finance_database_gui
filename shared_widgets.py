from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class ContentBox(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow_color = QColor("#000000")
        shadow_color.setAlpha(50)
        shadow.setColor(shadow_color)
        shadow.setOffset(QPointF(0, 4))
        self.setGraphicsEffect(shadow)

        self.setStyleSheet("border: 1px solid black")       


class SectionCard(QFrame):
    def __init__(
        self,
        color,
        text,
        description,
        icon,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName("section_card")
        self.setFixedSize(350, 250)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        self.header = CardHeader(text)
        self.layout.addWidget(self.header)

        self.description = QLabel(self)
        self.description.setAlignment(Qt.AlignAbsolute)
        self.description.setText(description)
        self.description.setObjectName("description")
        self.description.setWordWrap(True)
        self.description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.description.setCursor(Qt.IBeamCursor)
        self.layout.addWidget(self.description)

        self.button = QPushButton(self)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setFixedSize(80, 35)
        self.button.setText("Explore")
        self.layout.addWidget(self.button)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow_color = QColor("#000000")
        shadow_color.setAlpha(50)
        shadow.setColor(shadow_color)
        shadow.setOffset(QPointF(0, 4))
        self.setGraphicsEffect(shadow)

        if color == "blue":
            background = "#3971C6"
            font = "#FFFFFF"
            button = "#FFFFFF"
            button_font = "#3971C6"
            button_hovered = "#dcdfe3"
            button_pressed = "#babcbf"
        elif color == "white":
            background = "#FFFFFF"
            font = "#333333"
            button = "#3971C6"
            button_font = "#FFFFFF"
            button_hovered = "#2B5DA9"
            button_pressed = "#1D509C"

        self.setStyleSheet(
            f"""
            QFrame#section_card {{
                border: None;
                border-radius: 20px;
                background-color: {background};
                padding: 30px
            }}
            QLabel {{
                font-family: Lato;
                font-weight: bold;
                color: {font};
            }}
            QLabel#header {{
                font-size: 22px;
            }}
            QLabel#description {{
                font-size: 14px;
            }}
            QPushButton {{
                border: None;
                border-radius: 15px;
                background-color: {button};
                font-family: Lato;
                font-size: 14px;
                font-weight: bold;
                color: {button_font}
            }}
            QPushButton:hover {{
                background-color: {button_hovered}
            }}
            QPushButton:pressed {{
                background-color: {button_pressed}
            }}
            """
        )

class CardHeader(QLabel):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("header")
        self.setMaximumHeight(30)
        self.setText(text)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(Qt.IBeamCursor)

class CardButton(QLabel):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        self.setStyleSheet("border: 1px solid black")
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(Qt.IBeamCursor)

class SectionDescription(QLabel):
    def __init__(self, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(230)

        if color == "blue":
            font = "#FFFFFF"
            border = "#4A83D9"
        elif color == "white":
            font = "#333333"
            border = "#3971C6"

        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(Qt.IBeamCursor)

        self.setStyleSheet(
            f"""
            QLabel {{
                border: None;
                border-left: 5px solid {border};
                padding-left: 20px;
                font-family: Lato;
                font-size: 14px;
                font-weight: bold;
                color: {font}
            }}
            """
        )
        font = QFont()
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.05)
        self.setFont(font)

class SectionHeader(QLabel):
    def __init__(self, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if color == "blue":
            font = "#FFFFFF"
        elif color == "white":
            font = "#333333"
        
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(Qt.IBeamCursor)

        self.setStyleSheet(
            f"""
            QLabel {{
                font-family: Lato;
                font-size: 32px;
                font-weight: bold;
                color: {font};
            }}
            """
        )