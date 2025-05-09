from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content, align="left", color="black"):
        super().__init__()

        self.setWordWrap(True)
        if align == "left":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        elif align == "center":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setStyleSheet("color: {};".format(color))
        self.setText(content)


class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
