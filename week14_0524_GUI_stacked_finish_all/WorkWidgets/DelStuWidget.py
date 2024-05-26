from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent, CheckboxComponent, TextBrowserComponent
from SocketClient.ServiceController import ExecuteCommand
import json

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("del_stu_widget")

        # self.stu_message = {'name':'', 'scores':{}}

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Delete Student")
        name_label = LabelComponent(16, "Name: ")

        self.text_browser = TextBrowserComponent()
        # subject_label = LabelComponent(16, "Subject: ")
        # score_label = LabelComponent(16, "Score: ")
        self.user_hint_label = LabelComponent(16, "")
        self.user_hint_label.setStyleSheet("color: red;")

        self.name_combo_box = ComboBoxComponent("Select student")
        self.name_combo_box.currentTextChanged.connect(self.select_stu)

        # self.subject_editor_label = LineEditComponent("Subject")
        # self.subject_editor_label.mousePressEvent = lambda x: self.subject_editor_label.clear()
        # self.subject_editor_label.textChanged.connect(self.enable_button)

        # self.score_editor_label = LineEditComponent("")
        # self.score_editor_label.setValidator(QtGui.QIntValidator())
        # self.score_editor_label.mousePressEvent = lambda x: self.score_editor_label.clear()
        # self.score_editor_label.textChanged.connect(self.enable_button)

        self.confirm_check_box = CheckboxComponent("Confirm")
        self.confirm_check_box.clicked.connect(self.confirm_check_action)
        self.send_button = ButtonComponent("Send")
        self.send_button.clicked.connect(self.send_button_action)
        # self.query_button = ButtonComponent("Query")
        # self.query_button.clicked.connect(self.query_button_action)
        # self.add_button = ButtonComponent("Add")
        # self.add_button.clicked.connect(self.add_button_action)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.text_browser, 2, 0, 4, 4)
        # layout.addWidget(subject_label, 2, 0, 1, 1)
        # layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.user_hint_label, 0, 4, 4, 2)

        # layout.addWidget(self.name_editor_label, 1, 1, 1, 2)
        # layout.addWidget(self.subject_editor_label, 2, 1, 1, 2)
        # layout.addWidget(self.score_editor_label, 3, 1, 1, 2)

        # layout.addWidget(self.query_button, 1, 3, 1, 1)
        # layout.addWidget(self.add_button, 3, 3, 1, 1)
        layout.addWidget(self.confirm_check_box, 4, 4, 1, 2)
        layout.addWidget(self.send_button, 5, 4, 1, 2)

        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(4, 2)

        self.setLayout(layout)

        # self.initial_state()

    def initial_state(self):
        self.name_combo_box.setCurrentIndex(-1)
        self.confirm_check_box.setCheckable(False)
        self.confirm_check_box.setChecked(False)
        # self.name_editor_label.setText("Name")
        # self.subject_editor_label.setText("Subject")
        # self.score_editor_label.setText("")
        # self.query_button.setEnabled(False)
        # self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)
        # self.subject_editor_label.setEnabled(False)
        # self.score_editor_label.setEnabled(False)
        # self.name_editor_label.setEnabled(True)
        # self.stu_message = {'name':'', 'scores':{}}

    def get_stu_data(self):
        self.send_command = ExecuteCommand(command='show', data={})
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_stu_data)

    def process_stu_data(self, result):
        result = json.loads(result)

        self.text_browser.setText("") # clear
        self.text_browser.setText("==== student list ====")
        for _ , info in result['parameters'].items():
            for key , value in info.items():
                if key == 'name':
                    self.text_browser.append(f"\nName: {value}")
                elif key == 'scores':
                    for subject , score in value.items():
                        self.text_browser.append(f"  subject: {subject}, score: {score}")
        self.text_browser.append("\n==================")

    def select_stu(self, value):
        self.confirm_check_box.setCheckable(True)
        # TODO: print info

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

    def load(self):
        print('delete widget')
        self.initial_state()
        self.get_stu_data()