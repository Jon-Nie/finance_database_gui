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
        icon: url(icons/{0}_white.svg)
    }}
"""

sidebar_button_sub_css = """
    QPushButton {
        border: None;
        color: #A1A1A1;
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