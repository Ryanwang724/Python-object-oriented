from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent
from SocketClient.ServiceController import ExecuteCommand
import json
import copy
import os

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.delay_time = 2000 # ms
        self.enable_flag = True
        self.this_file_path = os.path.dirname(os.path.abspath(__file__))
        self.background_image_path = os.path.join(self.this_file_path, '..', 'Image', 'background', 'view.jpg') # 設定背景圖片
        self.background_pixmap = QtGui.QPixmap(self.background_image_path)
        self.setObjectName("modify_stu_widget")

        self.name_list = list()
        self.stu_score_dict = dict()

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Modify Student")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(16, "Subject: ")
        score_label = LabelComponent(16, "Score: ")
        self.user_hint_label = LabelComponent(16, "")
        self.user_hint_label.setStyleSheet("color: red;")

        self.name_combo_box = ComboBoxComponent("Select student")
        self.name_combo_box.currentTextChanged.connect(self.select_stu)

        self.subject_editor_label = LineEditComponent("Subject")
        self.subject_editor_label.mousePressEvent = lambda x: self.subject_editor_label.clear()
        self.subject_editor_label.textChanged.connect(self.enable_button)

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

        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.user_hint_label, 0, 4, 5, 2)

        layout.addWidget(self.name_combo_box, 1, 1, 1, 2)
        layout.addWidget(self.subject_editor_label, 2, 1, 1, 2)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 2)

        layout.addWidget(self.reset_button, 5, 0, 1, 2)
        layout.addWidget(self.send_button, 5, 4, 1, 2)

        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(4, 2)

        self.setLayout(layout)

        self.message_timer = QtCore.QTimer()
        self.message_timer.timeout.connect(self.clear_user_hint)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

    def initial_state(self):
        self.name_combo_box.setCurrentIndex(-1)
        self.subject_editor_label.setText("Subject")
        self.subject_editor_label.setEnabled(False)

        self.score_editor_label.setText("")
        self.score_editor_label.setEnabled(False)

        self.send_button.setEnabled(False)
        self.reset_button.setEnabled(False)

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
            self.name_combo_box.setEnabled(True and self.enable_flag)
        else:
            self.name_combo_box.setEnabled(False)
            if not self.user_hint_label.text():
                self.user_hint_label.setText("No student data, please go to Add.")

    def select_stu(self, value):
        if value in self.parameters.keys():
            self.reset_button.setEnabled(True)
            print_str = 'Current subject: \n'
            for subject,score in self.parameters[value]['scores'].items():
                print_str += f'    {subject} : {score}\n'
            self.user_hint_label.setText(print_str)
            self.subject_editor_label.setEnabled(True)
            self.subject_editor_label.setText('Subject')
            self.score_editor_label.setEnabled(True)

    def reset_button_action(self):
        self.initial_state()
        self.user_hint_label.setText("")

    def enable_button(self):
        self.reset_button.setEnabled(True)
        if len(self.subject_editor_label.text().strip()) > 0 and \
            len(self.score_editor_label.text().strip()) > 0:
            self.send_button.setEnabled(True)
        else:
            self.send_button.setEnabled(False)

    def send_button_action(self):
        student_name = self.name_combo_box.currentText()
        subject = self.subject_editor_label.text().strip()
        score = float(self.score_editor_label.text().strip())
        self.enable_flag = False
        self.stu_score_dict = copy.deepcopy(self.parameters[student_name]['scores'])
        self.stu_score_dict[subject] = score
        parameters = {'name':student_name, 'scores_dict':self.stu_score_dict}

        self.send_command = ExecuteCommand(command='modify', data=parameters)
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_result_send_button)

    def process_result_send_button(self, result):
        student_name = self.name_combo_box.currentText()
        subject = self.subject_editor_label.text().strip()
        score = self.score_editor_label.text().strip()

        result = json.loads(result)
        if result['status'] == 'OK':
            print_str = f'[{student_name},{subject},{score}] success.'
            if subject in self.parameters[student_name]['scores'].keys():
                self.user_hint_label.setText('Modify ' + print_str)
            else:
                self.user_hint_label.setText('Add ' + print_str)
            self.initial_state()
            self.get_stu_data()
            self.message_timer.start(self.delay_time)

    def clear_user_hint(self):
        self.user_hint_label.setText("")
        self.enable_flag = True
        self.name_combo_box.setEnabled(True and self.enable_flag)
        self.message_timer.stop()

    def load(self):
        print('Modify widget')
        self.initial_state()
        self.user_hint_label.setText("")
        self.get_stu_data()