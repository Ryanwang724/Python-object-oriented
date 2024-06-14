from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WebServiceClient.ServiceController import ExecuteCommand

import json


class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")
        self.scroll_area_content = ScrollAreaContentWidget()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scroll_area_content)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        layout.addWidget(header_label, stretch=1)
        layout.addWidget(scroll_area, stretch=9)

        self.setLayout(layout)
    
    def load(self):
        self.execute_show = ExecuteCommand(command="show", data=dict())
        self.execute_show.start()
        self.execute_show.return_sig.connect(self.show_action_result)

    def show_action_result(self, result):
        result = json.loads(result)
        info_result = str()

        if result['status'] == "OK":
            student_list = result['parameters']
            for student in student_list:
                info_result += "Name: {}\n".format(student['name'])
                for subject, score in student['scores'].items():
                    info_result += "  subject: {}, score: {}\n".format(subject, score)
                info_result += "\n"            
        else:
            info_result += "    Retrieve data fail"
        
        self.scroll_area_content.info_label.setText(info_result)


class ScrollAreaContentWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_scroll_area_widget")

        layout = QtWidgets.QVBoxLayout()

        self.title_label = LabelComponent(18, "==== student list ====")
        self.info_label = LabelComponent(16, "")
        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)

        self.setLayout(layout)
