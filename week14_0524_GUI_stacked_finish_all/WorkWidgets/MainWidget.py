from PyQt6 import QtWidgets, QtGui
import os
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.WidgetComponents import ButtonComponent


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.this_file_path = os.path.dirname(os.path.abspath(__file__))
        self.setObjectName("main_widget")

        self.setWindowTitle("Student Management System")
        title_icon_path = os.path.join(self.this_file_path, '..', 'Image', 'title', 'Elegantthemes-Beautiful-Flat-Stack.svg')
        self.setWindowIcon(QtGui.QIcon(title_icon_path))
        layout = QtWidgets.QGridLayout()
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)

        layout.addWidget(function_widget, 0, 0, 1, 1)
        layout.addWidget(menu_widget, 1, 0, 1, 1)

        self.setLayout(layout)

class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QHBoxLayout()
        self.buttons = {
            "add": ButtonComponent("Add student"),
            "modify": ButtonComponent("Modify student"),
            "delete": ButtonComponent("Delete student"),
            "show": ButtonComponent("Show all")
        }

        # https://medium.com/seaniap/python-lambda-函式-7e86a56f1996
        for name, button in self.buttons.items():
            button.clicked.connect(lambda checked, name=name: self.handle_button_click(name))
            layout.addWidget(button, stretch=1)

        self.setLayout(layout)
        self.update_button_styles("show") # 初始頁面

    def handle_button_click(self, widget_name):
        self.update_widget_callback(widget_name)
        self.update_button_styles(widget_name)

    def update_button_styles(self, active_widget_name):
        for name, button in self.buttons.items():
            if name == active_widget_name:
                button.setStyleSheet("background-color: yellow;") # 提示使用者所在頁面
            else:
                button.setStyleSheet("")

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.this_file_path = os.path.dirname(os.path.abspath(__file__))
        self.widget_dict = {
            "add": self.addWidget(AddStuWidget()),
            "modify": self.addWidget(ModifyStuWidget()),
            "delete": self.addWidget(DelStuWidget()),
            "show": self.addWidget(ShowStuWidget())
        }
        self.menu_widget = None
        self.update_widget("show") # 初始頁面

    def update_widget(self, widget_name):
        widget_index = self.widget_dict.get(widget_name)
        if widget_index is not None:
            self.setCurrentIndex(widget_index)
            current_widget = self.currentWidget()
            current_widget.load()
            if self.menu_widget:
                self.menu_widget.update_button_styles(widget_name)
        else:
            print(f"Error: The widget '{widget_name}' does not exist.")
    
    def set_menu_widget(self, menu_widget):
        self.menu_widget = menu_widget