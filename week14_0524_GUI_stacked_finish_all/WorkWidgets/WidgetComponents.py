from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("微軟正黑體", font_size))
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

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, text):
        super().__init__()
        self.setPlaceholderText(text)
        self.setCurrentIndex(-1)
        self.setFixedHeight(35)
        self.setFixedWidth(200)
        self.setStyleSheet("font-size: 16px;")

class CheckboxComponent(QtWidgets.QCheckBox):
    def __init__(self, text):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", 16))
        self.setEnabled(False)
        self.setCheckable(True)
        self.setChecked(False)
        self.setText(text)
        self.setStyleSheet("""
                           QCheckBox::indicator {
                               width: 20px;
                               height: 20px;
                           }
                           """)

class ScrollAreaComponent(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.content = LabelComponent(16, "")
        self.setWidget(self.content)