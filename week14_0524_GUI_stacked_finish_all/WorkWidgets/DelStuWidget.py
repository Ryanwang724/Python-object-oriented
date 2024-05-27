from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent, CheckboxComponent, TextBrowserComponent
from SocketClient.ServiceController import ExecuteCommand
import json

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("del_stu_widget")

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Delete Student")
        name_label = LabelComponent(16, "Name: ")

        self.text_browser = TextBrowserComponent()

        self.user_hint_label = LabelComponent(16, "")
        self.user_hint_label.setStyleSheet("color: red;")

        self.name_combo_box = ComboBoxComponent("Select student")
        self.name_combo_box.currentTextChanged.connect(self.select_stu)

        self.confirm_check_box = CheckboxComponent("Confirm")
        self.confirm_check_box.stateChanged.connect(self.confirm_check_action)
        self.send_button = ButtonComponent("Send")
        self.send_button.clicked.connect(self.send_button_action)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_combo_box, 1, 1, 1, 2)
        layout.addWidget(self.text_browser, 2, 0, 4, 4)

        layout.addWidget(self.user_hint_label, 0, 4, 4, 2)

        layout.addWidget(self.confirm_check_box, 4, 4, 1, 2)
        layout.addWidget(self.send_button, 5, 4, 1, 2)

        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(4, 2)

        self.setLayout(layout)

    def initial_state(self):
        self.name_combo_box.setCurrentIndex(-1)
        self.confirm_check_box.setEnabled(False)
        self.confirm_check_box.setChecked(False)
        self.send_button.setEnabled(False)

    def get_stu_data(self):
        self.send_command = ExecuteCommand(command='show', data={})
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_stu_data)

    def process_stu_data(self, result):
        result = json.loads(result)
        self.parameters = result['parameters']
        self.name_list = list()

        for name in self.parameters.keys():
            self.name_list.append(name)

        if len(self.name_list) > 0:
            self.name_combo_box.clear()
            self.name_combo_box.addItems(self.name_list)
            self.name_combo_box.setEnabled(True)
            self.user_hint_label.setText("")
        else:
            self.name_combo_box.setEnabled(False)
            self.user_hint_label.setText("No student data, please go to Add.")
        self.show_data(self.parameters)

    def show_data(self, data):
        self.text_browser.setText("") # clear
        self.text_browser.setText("==== student list ====")
        for _ , info in data.items():
            for key , value in info.items():
                if key == 'name':
                    self.text_browser.append(f"\nName: {value}")
                elif key == 'scores':
                    for subject , score in value.items():
                        self.text_browser.append(f"  subject: {subject}, score: {score}")
        self.text_browser.append("\n==================")

    def select_stu(self, value):
        if value in self.parameters.keys():
            self.confirm_check_box.setEnabled(True)
            print_data = dict()
            print_data[value] = self.parameters[value]
            self.show_data(print_data)

    def confirm_check_action(self, state):
        state = QtCore.Qt.CheckState(state)
        if state == QtCore.Qt.CheckState.Unchecked:
            self.send_button.setEnabled(False)
        elif state == QtCore.Qt.CheckState.Checked:
            self.send_button.setEnabled(True)

    def send_button_action(self):
        student_name = self.name_combo_box.currentText()
        parameters = {'name':student_name}

        self.send_command = ExecuteCommand(command='delete', data=parameters)
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_result_send_button)

    def process_result_send_button(self, result):
        result = json.loads(result)
        if result['status'] == 'OK':
            self.user_hint_label.setText(f"Delete success")
            self.initial_state()
            self.get_stu_data()
            self.show_data(self.parameters)

    def load(self):
        print('delete widget')
        self.initial_state()
        self.get_stu_data()