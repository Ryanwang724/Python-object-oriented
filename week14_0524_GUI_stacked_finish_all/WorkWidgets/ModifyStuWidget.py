from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, RadioButtonComponent, ComboBoxComponent
from SocketClient.ServiceController import ExecuteCommand
import json

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("modify_stu_widget")

        # self.stu_message = {'name':'', 'scores':{}}
        self.stu_message = dict()
        self.name_list = list()

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Modify Student")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(16, "Subject: ")
        score_label = LabelComponent(16, "Score: ")
        self.user_hint_label = LabelComponent(16, "")
        self.user_hint_label.setStyleSheet("color: red;")

        self.name_combo_box = ComboBoxComponent("Select student")
        # self.add_new_radio_button = RadioButtonComponent("Add new", 16)
        # self.change_radio_button = RadioButtonComponent("Change", 16)

        self.subject_combo_box = ComboBoxComponent("Select subject")

        self.score_editor_label = LineEditComponent("")
        self.score_editor_label.setValidator(QtGui.QIntValidator())
        self.score_editor_label.mousePressEvent = lambda x: self.score_editor_label.clear()
        self.score_editor_label.textChanged.connect(self.enable_button)

        self.send_button = ButtonComponent("Send")
        self.send_button.clicked.connect(self.send_button_action)

        self.reset_button = ButtonComponent("Reset")
        self.reset_button.clicked.connect(self.reset_button_action)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        # layout.addWidget(self.add_new_radio_button, 2, 0, 1, 1)
        # layout.addWidget(self.change_radio_button, 2, 1, 1, 1)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.user_hint_label, 0, 4, 4, 2)

        layout.addWidget(self.name_combo_box, 1, 1, 1, 2)
        layout.addWidget(self.subject_combo_box, 2, 1, 1, 2)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 2)

        layout.addWidget(self.reset_button, 5, 0, 1, 2)
        layout.addWidget(self.send_button, 5, 4, 1, 2)

        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(4, 2)

        self.setLayout(layout)

        self.get_stu_data()
        self.name_combo_box.addItems(self.name_list)

        # self.initial_state()

    def get_stu_data(self):
        self.send_command = ExecuteCommand(command='show', data={})
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_data)

    def process_data(self, result):
        result = json.loads(result)
        self.name_list = list()
        self.subject_list = list()
        self.subject_dict = dict()
        
        for name , info in result['parameters'].items():
            self.name_list.append(name)
            for key , value in info.items():
                if key == 'scores':
                    for subject , score in value.items():
                        self.subject_list.append(subject)
            self.subject_dict[name] = self.subject_list

    def initial_state(self):
        self.stu_message = dict()
        self.get_stu_data()
        self.name_combo_box.clear()
        self.name_combo_box.addItems(self.name_list)

        # self.add_new_radio_button.setEnabled(False)
        # self.change_radio_button.setEnabled(False)

        self.subject_combo_box.setEnabled(False)

        self.score_editor_label.setText("")
        self.score_editor_label.setEnabled(False)

        self.send_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def reset_button_action(self):
        self.initial_state()

    def send_button_action(self):
        parameters = self.stu_message

        self.send_command = ExecuteCommand(command='modify', data=parameters)
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
        elif sender is self.score_editor_label or sender is self.subject_editor_label:
            if len(self.subject_editor_label.text().strip()) != 0 and len(self.score_editor_label.text().strip()) != 0:
                flag = True
            else:
                flag = False
            self.add_button.setEnabled(flag)
    
    def process_result_send_button(self, result):
        result = json.loads(result)
        if result['status'] == 'OK':
            self.user_hint_label.setText(f"The information {self.stu_message} is sent.")
            self.initial_state()

    def load(self):
        print('Modify widget')
        self.initial_state()