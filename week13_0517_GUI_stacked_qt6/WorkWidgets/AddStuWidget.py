from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from SocketClient.ServiceController import ExecuteCommand
import json

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")

        self.stu_message = {'name':'', 'scores':{}}

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Add Student")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(16, "Subject: ")
        score_label = LabelComponent(16, "Score: ")
        self.user_hint_label = LabelComponent(16, "")
        self.user_hint_label.setStyleSheet("color: red;")

        self.name_editor_label = LineEditComponent("Name")
        self.name_editor_label.mousePressEvent =  lambda x: self.name_editor_label.clear()
        self.name_editor_label.textChanged.connect(self.enable_button)
        self.subject_editor_label = LineEditComponent("Subject")
        self.subject_editor_label.mousePressEvent = lambda x: self.subject_editor_label.clear()
        self.score_editor_label = LineEditComponent("")
        self.score_editor_label.setValidator(QtGui.QIntValidator())
        self.score_editor_label.mousePressEvent = lambda x: self.score_editor_label.clear()
        self.score_editor_label.textChanged.connect(self.enable_button)

        self.send_button = ButtonComponent("Send")
        self.send_button.clicked.connect(self.send_button_action)
        self.query_button = ButtonComponent("Query")
        self.query_button.clicked.connect(self.query_button_action)
        self.add_button = ButtonComponent("Add")
        self.add_button.clicked.connect(self.add_button_action)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.user_hint_label, 0, 4, 4, 2)

        layout.addWidget(self.name_editor_label, 1, 1, 1, 2)
        layout.addWidget(self.subject_editor_label, 2, 1, 1, 2)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 2)

        layout.addWidget(self.query_button, 1, 3, 1, 1)
        layout.addWidget(self.add_button, 3, 3, 1, 1)
        layout.addWidget(self.send_button, 5, 4, 1, 2)

        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(4, 2)

        self.setLayout(layout)

        self.initial_state()

    def initial_state(self):
        self.name_editor_label.setText("Name")
        self.subject_editor_label.setText("Subject")
        self.score_editor_label.setText("")
        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)
        self.name_editor_label.setEnabled(True)
        self.stu_message = {'name':'', 'scores':{}}

    def query_button_action(self):
        parameters = {'name':self.name_editor_label.text()}

        self.send_command = ExecuteCommand(command='query', data=parameters)
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_result_query_button)

    def add_button_action(self):
        self.stu_message['name'] = self.name_editor_label.text()
        self.stu_message['scores'][self.subject_editor_label.text()] = self.score_editor_label.text()
        self.user_hint_label.setText(f"Student {self.name_editor_label.text()}'s subject '{self.subject_editor_label.text()}' with score '{self.score_editor_label.text()}' added")

        self.name_editor_label.setEnabled(False)
        self.send_button.setEnabled(True)
        self.subject_editor_label.clear()
        self.score_editor_label.clear()

    def send_button_action(self):
        parameters = self.stu_message

        self.send_command = ExecuteCommand(command='add', data=parameters)
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_result_send_button)

    def enable_button(self):
        sender = self.sender()
        if len(sender.text().strip()) > 0:  # 避免空字串
            flag = True
        else:
            flag = False

        if sender is self.name_editor_label:
            self.query_button.setEnabled(flag)
        elif sender is self.score_editor_label:
            self.add_button.setEnabled(flag)

    def process_result_query_button(self, result):
        result = json.loads(result)
        if result['status'] == 'Fail':
            self.user_hint_label.setText(f"Please enter subjects for student '{self.name_editor_label.text()}'")
            self.name_editor_label.setEnabled(False)
            self.subject_editor_label.setEnabled(True)
            self.score_editor_label.setEnabled(True)
            self.query_button.setEnabled(False)
            self.send_button.setEnabled(False)
        else:
            self.user_hint_label.setText(f'student {self.name_editor_label.text()} is already exist.')
            self.initial_state()
    
    def process_result_send_button(self, result):
        result = json.loads(result)
        if result['status'] == 'OK':
            self.user_hint_label.setText(f"The information {self.stu_message} is sent.")
            self.initial_state()

    def load(self):
        print('Add widget')
        self.initial_state()