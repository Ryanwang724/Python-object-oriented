from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")

        self.message = {}

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Add Student")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(16, "Subject: ")
        score_label = LabelComponent(16, "Score: ")
        self.user_hint_label = LabelComponent(16, "")
        self.user_hint_label.setStyleSheet("color: red;")

        self.name_editor_label = LineEditComponent("Name")
        self.name_editor_label.mousePressEvent = self.clear_editor_content
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
        layout.addWidget(self.user_hint_label, 0, 4, 2, 2)

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

    def clear_editor_content(self, event):
        self.name_editor_label.clear()

    def initial_state(self):
        self.name_editor_label.setText("Name")
        self.subject_editor_label.setText("Subject")
        self.score_editor_label.setText("")
        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)

    def query_button_action(self):
        self.user_hint_label.setText(f"Please enter subjects for student '{self.name_editor_label.text()}'")
        self.subject_editor_label.setEnabled(True)
        self.score_editor_label.setEnabled(True)
        self.query_button.setEnabled(False)

    def add_button_action(self):
        name = self.name_editor_label.text()
        score = {self.subject_editor_label.text() : self.score_editor_label.text()}
        self.message = {'name':name, 'scores': score}
        self.user_hint_label.setText(f"Student {self.name_editor_label.text()}'s subject '{self.subject_editor_label.text()}' with score '{self.score_editor_label.text()}' added")

    def send_button_action(self):
        print(self.message)
        self.user_hint_label.setText(f"The information {self.message} is sent.")
        self.initial_state()

    def enable_button(self):
        sender = self.sender()
        if sender is self.name_editor_label:
            self.query_button.setEnabled(True)
        elif sender is self.score_editor_label:
            self.add_button.setEnabled(True)