app_css = """
    QFrame {
        background-color: #F7F8FD
    }
"""

grip_css = """
    QSizeGrip {
        background-color: transparent
    }
"""

sidebar_css = """
    QFrame {
        background-color: #386BB7
    }
"""

sidebar_placeholder_css = """
    QFrame {
        background-color: #386BB7;
    }
    QFrame#wrapper_top {
        border-bottom-right-radius: 20px;
    }
    QFrame#wrapper_bottom {
        border-top-right-radius: 20px;
    }
"""

sidebar_button_css = """
    QPushButton {{
        border: None;
        background-color: #386BB7;
        icon: url(icons/{0}_white.svg);
        qproperty-iconSize: 25px
    }}
    QPushButton:hover {{
        background-color: #2B5DA9
    }}
    QPushButton:pressed {{
        background-color: #1D509C
    }}
    QPushButton#active {{
        background-color: transparent;
        icon: url(icons/{0}_blue.svg);
        qproperty-iconSize: 25px
    }}
    QPushButton#wrapper_top {{
        border-bottom-right-radius: 20px;
    }}
    QPushButton#wrapper_bottom {{
        border-top-right-radius: 20px;
    }}
"""

topbar_css = """
    QFrame {
        background-color: transparent;
    }
"""

search_box_css = """
    QLineEdit {
        font-family: Lato;
        font-size: 14px;
        background-color: #FFFFFF;
        color: black;
        border-radius: 2px;
        border: 1px solid #E2E2E2;
        padding: 0px 10px 0px 10px;
        margin: 7px 0px 7px 0px;
    }
"""

minimize_css = """
    QPushButton {
        border: None;
        padding: 15px 10px 10px 10px;
        icon: url(icons/minimize.svg);
        qproperty-iconSize: 20px
    }
    QPushButton:hover {
        background-color: #dcdfe3;
    }
    QPushButton:pressed {
        background-color: #babcbf;
    }
"""

maximize_css = """
    QPushButton {
        border: None;
        padding: 12.5px;
        icon: url(icons/maximize.svg);
        qproperty-iconSize: 20px
    }
    QPushButton:hover {
        background-color: #dcdfe3;
    }
    QPushButton:pressed {
        background-color: #babcbf;
    }
"""

close_css = """
    QPushButton {
        border: None;
        padding:10px;
        icon: url(icons/close_black.svg);
        qproperty-iconSize: 20px
    }
    QPushButton:hover {
        background-color: #ed3b3b;
        icon: url(icons/close_white.svg);
        qproperty-iconSize: 20px
    }
    QPushButton:hover:pressed {
        background-color: #a32222;
        icon: url(icons/close_white.svg);
        qproperty-iconSize: 20px
    }
"""