from PyQt6 import QtWidgets, QtGui, QtCore
import os
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.WidgetComponents import LabelComponent
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
        header_label = LabelComponent(24, "Student Management System")
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)

        # background_image_path = os.path.join(self.this_file_path, '..', 'Image', 'background', 'blue.jpg')

        # if os.path.exists(background_image_path):
        #     # 使用正確的路徑格式
        #     background_image_path = background_image_path.replace('\\', '/')
        #     self.setStyleSheet(f'background-image: url("{background_image_path}");')
        # else:
        #     print(f"Error: The background image {background_image_path} does not exist.")

        # layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(function_widget, 0, 0, 1, 1)
        layout.addWidget(menu_widget, 1, 0, 1, 1)

        # layout.setColumnStretch(0, 1)
        # layout.setColumnStretch(1, 6)
        # layout.setRowStretch(0, 1)
        # layout.setRowStretch(1, 6)

        self.setLayout(layout)

    # def set_background(self, event):
    #     painter = QtGui.QPainter(self)

    #     background_image_path = os.path.join(self.this_file_path, '..', 'Image', 'background', 'blue.jpg')
    #     print(background_image_path)
    #     if os.path.exists(background_image_path):
    #         # 使用正確的路徑格式
    #         background_image_path = background_image_path.replace('\\', '/')
    #         self.setStyleSheet(f'background-image: url("{background_image_path}");')
    #     else:
    #         print(f"Error: The background image {background_image_path} does not exist.")
    #     pixmap = QtGui.QPixmap(background_image_path)
    #     painter.drawPixmap(self.rect(), pixmap)
    #     super().set_background(event)


class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QHBoxLayout()
        add_button = ButtonComponent("Add student")
        modify_button = ButtonComponent("Modify student")
        delete_button = ButtonComponent("Delete student")
        show_button = ButtonComponent("Show all")
        # https://medium.com/seaniap/python-lambda-函式-7e86a56f1996
        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))
        delete_button.clicked.connect(lambda: self.update_widget_callback("delete"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))

        layout.addWidget(add_button, stretch=1)
        layout.addWidget(modify_button, stretch=1)
        layout.addWidget(delete_button, stretch=1)
        layout.addWidget(show_button, stretch=1)

        self.setLayout(layout)


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
        self.img_dict = {
            'add':'green.png',
            'modify':'red.jpg',
            'delete':'yellow.jpg',
            'show':'pink.jpg'
        }
        background_image_path = os.path.join(self.this_file_path, '..', 'Image', 'background', 'green.png')

        if os.path.exists(background_image_path):
            # 使用正確的路徑格式
            background_image_path = background_image_path.replace('\\', '/')
            self.setStyleSheet(f'background-image: url("{background_image_path}");')
        else:
            print(f"Error: The background image {background_image_path} does not exist.")
        self.update_widget("add")
    
    # def update_widget(self, name):
    #     self.setCurrentIndex(self.widget_dict[name])
    #     current_widget = self.currentWidget()
    #     current_widget.load()

    def update_widget(self, widget_name):
        widget_index = self.widget_dict.get(widget_name)
        if widget_index is not None:
            self.setCurrentIndex(widget_index)
            current_widget = self.currentWidget()
            current_widget.load()
            background_image_path = os.path.join(
                self.this_file_path, '..', 'Image', 'background', self.img_dict[widget_name]
            )
            self.update_background_image(background_image_path)
            # if os.path.exists(background_image_path):
            #     background_image_path = background_image_path.replace('\\', '/')
            #     self.setStyleSheet(f'background-image: url("{background_image_path}");')
            # else:
            #     print(f"Error: The background image {background_image_path} does not exist.")
        else:
            print(f"Error: The widget '{widget_name}' does not exist.")

    def update_background_image(self, image_path):
        if os.path.exists(image_path):
            image_path = image_path.replace('\\', '/')
            self.setStyleSheet(f'''
                FunctionWidget {{
                    background-image: url("{image_path}");
                }}
                QPushButton {{
                    background: none;
                }}
            ''')
        else:
            print(f"Error: The background image {image_path} does not exist.")