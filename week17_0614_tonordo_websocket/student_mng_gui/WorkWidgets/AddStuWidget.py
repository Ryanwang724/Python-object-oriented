from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WebServiceClient.ServiceController import ExecuteCommand
import json


class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")

        layout = QtWidgets.QHBoxLayout()

        self.add_stu_status_widget = AddStuStatusWidget()
        self.add_stu_control_widget = AddStuControlWidget(self.add_stu_status_widget.status_widget)

        self.add_stu_status_widget.get_add_dict_callback = self.add_stu_control_widget.get_add_dict
        self.add_stu_status_widget.init_control_widget_callback = self.add_stu_control_widget.init_status

        layout.addWidget(self.add_stu_control_widget, stretch=2)
        layout.addWidget(self.add_stu_status_widget, stretch=1)

        self.setLayout(layout)

    def load(self):
        pass

class AddStuStatusWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.get_add_dict_callback = None
        self.init_control_widget_callback = None

        self.setObjectName("add_stu_status_widget")

        layout = QtWidgets.QVBoxLayout()

        self.status_widget = LabelComponent(16, "", "left", "red")
        self.send_button = ButtonComponent("Send", 16)
        self.send_button.clicked.connect(self.send_action)

        layout.addWidget(self.status_widget, stretch=2)
        layout.addWidget(self.send_button, stretch=1)

        self.setLayout(layout)

    def send_action(self):
        self.add_dict = self.get_add_dict_callback()
        if len(self.add_dict) > 0:
            self.execute_add = ExecuteCommand(command="add", data=self.add_dict)
            self.execute_add.start()
            self.execute_add.return_sig.connect(self.add_action_result)
        else:
            self.status_widget.setText("Please input correct information.")

    def add_action_result(self, result):
        result = json.loads(result)
        if result['status'] == "OK":
            self.status_widget.setText("Add {} successfully".format(self.add_dict))
        else:
            self.status_widget.setText("Add Fail")
        self.init_control_widget_callback()


class AddStuControlWidget(QtWidgets.QWidget):
    def __init__(self, status_shower_callback):
        super().__init__()
        self.setObjectName("add_new_stu_control_widget")
        self.status_shower_callback = status_shower_callback
        self.add_dict = dict()

        layout = QtWidgets.QGridLayout()
        
        header_label = LabelComponent(22, "Add Student", align="left")
        layout.addWidget(header_label, 0, 0, 1, 3)

        name_label = LabelComponent(18, "Name: ", align="center")
        self.name_editor = LineEditComponent("Name")
        self.name_editor.mousePressEvent = self.clear_name_editor_content
        self.query_button = ButtonComponent("Query")
        self.query_button.clicked.connect(self.query_action)
        self.query_button.setEnabled(False)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_editor, 1, 1, 1, 1)
        layout.addWidget(self.query_button, 1, 2, 1, 1)

        subject_label = LabelComponent(16, "Subject: ", align="center")
        self.subject_editor = LineEditComponent("Subject")
        self.subject_editor.mousePressEvent = self.clear_subject_editor_content
        self.subject_editor.setEnabled(False)

        score_label = LabelComponent(16, "Score: ", align="center")
        self.score_editor = LineEditComponent("Score")
        self.score_editor.mousePressEvent = self.clear_score_editor_content
        self.score_editor.setInputMask("999")
        self.score_editor.setEnabled(False)

        self.add_button = ButtonComponent("Add")
        self.add_button.clicked.connect(self.add_action)
        self.add_button.setEnabled(False)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_editor, 2, 1, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.score_editor, 3, 1, 1, 1)
        layout.addWidget(self.add_button, 3, 2, 1, 1)

        layout.setRowStretch(0, 10)
        layout.setRowStretch(1, 30)
        layout.setRowStretch(2, 30)
        layout.setRowStretch(3, 30)
        layout.setRowStretch(4, 30)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 2)

        self.setLayout(layout)

    def clear_name_editor_content(self, event):
        self.name_editor.clear()
        self.query_button.setEnabled(True)

    def clear_subject_editor_content(self, event):
        if self.add_dict.get('name') is not None:
            self.subject_editor.clear()
            self.add_button.setEnabled(True)
        else:
            self.status_shower_callback.setText("Please query a new name first")

    def clear_score_editor_content(self, event):
        if self.add_dict.get('name') is not None:
            self.score_editor.clear()
            self.add_button.setEnabled(True)
        else:
            self.status_shower_callback.setText("Please query a new name first")

    def query_action(self):
        if len(self.name_editor.text()) > 0:
            query_data = {"name": self.name_editor.text()}
            self.execute_query = ExecuteCommand(command="query", data=query_data)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.query_action_result)
            self.subject_editor.setEnabled(True)
            self.score_editor.setEnabled(True)

    def query_action_result(self, result):
        result = json.loads(result)
        if result['status'] != "OK":
            self.status_shower_callback.setText("Please enter subjects for student '{}'".format(self.name_editor.text()))
            self.query_button.setEnabled(False)
            self.add_dict['name'] = self.name_editor.text()
            self.add_dict['scores'] = dict()
        else:
            self.status_shower_callback.setText("The student '{}' already exists in DB".format(self.name_editor.text()))
            self.init_status()

    def add_action(self):
        name = self.add_dict['name']
        subject_name = self.subject_editor.text()
        score = self.score_editor.text()
        
        if len(subject_name)>0 and len(score)>0:
            self.status_shower_callback.setText("Student {}'s subject '{}' with score '{}' added".format(name, subject_name, score))
            self.add_dict['scores'][subject_name] = score
        else:
            self.status_shower_callback.setText("Subject or score is empty.".format(name, subject_name, score))

    def init_status(self):
        self.name_editor.setText("Name")
        self.subject_editor.setText("Subject")
        self.score_editor.clear()

        self.add_button.setEnabled(False)
        self.query_button.setEnabled(False)

        self.subject_editor.setEnabled(False)
        self.score_editor.setEnabled(False)
        
        self.add_dict = dict()

    def get_add_dict(self):
        if self.add_dict.get('name') is not None and len(self.add_dict.get('scores')) > 0:
            return self.add_dict
        else:
            return dict()

