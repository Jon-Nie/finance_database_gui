app_css = """
    QFrame {
        background-color: #FFFFFF
    }
"""

sidebar_css = """
    QFrame {
        background-color: #161A28
    }
"""



sidebar_button_css = """
    QPushButton {{
        font-family: Lato;
        font-size: 14px;
        text-align: left;
        font-weight: regular;
        color: #A1A1A1;
        border: None;
        padding: 10px 0px 10px 15px;
        icon: url(icons/{0}_grey.svg);
        qproperty-iconSize: 20px
    }}

    QPushButton:hover {{
        color: #FFFFFF;
        background-color: #20263A;
        icon: url(icons/{0}_white.svg)
    }}

    QPushButton:pressed {{
        color: #FFFFFF;
        background-color: #161A28;
        icon: url(icons/{0}_white.svg)
    }}

    QPushButton#active {{
        font-family: Lato;
        font-size: 14px;
        text-align: left;
        font-weight: regular;
        color: #FFFFFF;
        background-color: #20263A;
        border: None;
        border-left: 3px solid #FFFFFF;
        padding: 10px 0px 10px 12px;
        icon: url(icons/{0}_white.svg)
    }}
"""

sidebar_button_super_css = """
    QPushButton {{
        font-family: Lato;
        font-size: 14px;
        text-align: left;
        font-weight: regular;
        color: #A1A1A1;
        border: None;
        padding: 10px 0px 10px 15px;
        icon: url(icons/{0}_grey.svg);
        qproperty-iconSize: 20px
    }}

    QPushButton:hover {{
        color: #FFFFFF;
        background-color: #20263A;
        icon: url(icons/{0}_white.svg)
    }}

    QPushButton:pressed {{
        color: #FFFFFF;
        background-color: #161A28;
        icon: url(icons/{0}_white.svg)
    }}

    QPushButton#active {{
        color: #FFFFFF;
        background-color: #20263A;
        icon: url(icons/{0}_white.svg)
    }}
"""

sidebar_button_sub_css = """
    QPushButton {
        border: None;
        color: #A1A1A1;
        background-color: #20263A;
        font-family: Lato;
        font-size: 13px;
        text-align: left;
        font-weight: regular;
        padding: 0px 0px 0px 40px;
    }

    QPushButton:hover {
        color: #FFFFFF;
        background-color: #20263A;
    }

    QPushButton:pressed {
        color: #FFFFFF;
        background-color: #161A28;
    }

    QPushButton#active {
        border-left: 3px solid #FFFFFF;
        color: #FFFFFF;
        background-color: #20263A;
        padding: 0px 0px 0px 37px;
    }
"""

search_box_css = """
    QLineEdit {
        font-family: Lato;
        font-size: 14px;
        background-color: #FFFFFF;
        color: black;
        border-radius: 5px;
        border: 1px solid #a8a8a8;
        padding: 0px 10px 0px 10px;
        margin: 7px 0px 7px 0px
    }
"""

minimize_css = """
    QPushButton {
        border: None;
        padding: 15px 10px 10px 10px;
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

scrollarea_css = """
    QScrollArea {
        border: None
    }
    QScrollBar:handle {
        border: None;
        background-color: #d4d4d4;
        border-radius: 3px;
    }
    QScrollBar:handle:hover {
        background-color: #ababab;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background-color: #F6F8FB;
    }
"""