from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WebServiceClient.ServiceController import ExecuteCommand
import json


class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("modify_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Modify Student")
        self.modify_widget = ModifyWidget()

        layout.addWidget(header_label, stretch=1)
        layout.addWidget(self.modify_widget, stretch=8)
        self.setLayout(layout)
    
    def load(self):
        self.modify_widget.modify_info_widget.init_modify_page()
        self.modify_widget.status_shower.setText("")


class ModifyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("modify_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        self.status_shower = LabelComponent(18, "", align="center")
        self.modify_info_widget = ModifyInfoWidget(self.status_shower)
        self.query_info_widget = QueryInfoWidget(self.status_shower, self.modify_info_widget.init_combo_box)
        self.modify_info_widget.init_query_info_widget_callback = self.query_info_widget.init_status

        layout.addWidget(self.status_shower, stretch=1)
        layout.addWidget(self.query_info_widget, stretch=3)
        layout.addWidget(self.modify_info_widget, stretch=8)
        self.setLayout(layout)


class QueryInfoWidget(QtWidgets.QWidget):
    def __init__(self, status_shower_callback, init_combo_box_callback):
        super().__init__()
        self.setObjectName("query_info_widget")
        self.init_combo_box_callback = init_combo_box_callback
        self.status_shower_callback = status_shower_callback

        layout = QtWidgets.QHBoxLayout()

        name_label = LabelComponent(18, "Name: ", align="center")
        self.name_editor = LineEditComponent("Name")
        self.name_editor.mousePressEvent = self.clear_name_editor_content
        self.query_button = ButtonComponent("Query")
        self.query_button.clicked.connect(self.query_action)
        self.query_button.setEnabled(False)
        layout.addWidget(name_label, stretch=1)
        layout.addWidget(self.name_editor, stretch=3)
        layout.addWidget(self.query_button, stretch=2)

        self.setLayout(layout)

    def clear_name_editor_content(self, event):
        self.name_editor.clear()
        self.query_button.setEnabled(True)

    def query_action(self):
        if len(self.name_editor.text()) > 0:
            query_data = {"name": self.name_editor.text()}
            self.execute_query = ExecuteCommand(command="query", data=query_data)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.query_action_result)

    def query_action_result(self, result):
        result = json.loads(result)
        if result['status'] == "OK":
            self.query_button.setEnabled(False)
            self.init_combo_box_callback(self.name_editor.text(), result)
        else:
            self.status_shower_callback.setText("The student '{}' not exists in DB".format(self.name_editor.text()))
            self.init_status()

    def init_status(self):
        self.name_editor.setText("Name")
        self.query_button.setEnabled(False)


class ModifyInfoWidget(QtWidgets.QWidget):
    def __init__(self, status_shower_callback):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        self.stored_scores = dict()
        self.status_shower_callback = status_shower_callback
        self.init_query_info_widget_callback = None

        layout = QtWidgets.QGridLayout()

        self.radio_button_change = QtWidgets.QRadioButton('Change a current score:')
        self.radio_button_add = QtWidgets.QRadioButton('Add a new score:')

        self.radio_button_change.toggled.connect(self.radio_button_on_clicked)
        self.radio_button_add.toggled.connect(self.radio_button_on_clicked)

        self.combo_box_score = QtWidgets.QComboBox()
        self.combo_box_score.currentIndexChanged.connect(self.combo_box_select_changed)
        self.change_score_editor = LineEditComponent("")
        self.change_score_editor.setInputMask("999")

        add_subject_label = LabelComponent(16, "Subject: ", align="center")
        self.add_subject_editor = LineEditComponent("Subject")
        self.add_subject_editor.mousePressEvent = self.clear_add_subject_editor_content
        add_score_label = LabelComponent(16, "Score: ", align="center")
        self.add_score_editor = LineEditComponent("Score")
        self.add_score_editor.mousePressEvent = self.clear_add_score_editor_content
        self.add_score_editor.setInputMask("999")

        self.confirm_button = ButtonComponent("Confirm")
        self.confirm_button.clicked.connect(self.confirm_action)

        layout.addWidget(self.radio_button_change, 0, 0, 1, 3)
        layout.addWidget(self.combo_box_score, 1, 0, 1, 1)
        layout.addWidget(self.change_score_editor, 1, 1, 1, 1)
        layout.addWidget(self.radio_button_add, 2, 0, 1, 3)
        layout.addWidget(add_subject_label, 3, 0, 1, 1)
        layout.addWidget(self.add_subject_editor, 3, 1, 1, 1)
        layout.addWidget(add_score_label, 4, 0, 1, 1)
        layout.addWidget(self.add_score_editor, 4, 1, 1, 1)
        layout.addWidget(self.confirm_button, 5, 2, 1, 1)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 1)

        self.setLayout(layout)

    def radio_button_on_clicked(self):
        selected_button = self.sender()
        if selected_button.isChecked():
            print("{}".format(selected_button.text()))

    def combo_box_select_changed(self, index):
        if len(self.combo_box_score.currentText()) > 0:
            self.change_score_editor.setText(str(int(self.stored_scores[self.combo_box_score.currentText()])))
            self.radio_button_change.setChecked(True)

    def init_combo_box(self, name, score_list):
        self.stored_name = name
        self.stored_scores = score_list['scores']
        self.combo_box_score.clear()
        current_score_names = [keys for keys in score_list['scores']]
        self.combo_box_score.addItems(current_score_names)
        self.combo_box_score.update()

    def clear_add_subject_editor_content(self, event):
        self.add_subject_editor.clear()
        self.radio_button_add.setChecked(True)

    def clear_add_score_editor_content(self, event):
        self.add_score_editor.setText("0")
        self.radio_button_add.setChecked(True)

    def confirm_action(self):
        try:
            if self.radio_button_add.isChecked():
                self.stored_scores[self.add_subject_editor.text()] = int(self.add_score_editor.text())
            elif self.radio_button_change.isChecked():
                self.stored_scores[self.combo_box_score.currentText()] = int(self.change_score_editor.text())
            else:
                return
        except Exception as e:
            return

        modify_date = {
            'name': self.stored_name,
            'scores_dict': self.stored_scores
        }

        self.execute_modify = ExecuteCommand(command="modify", data=modify_date)
        self.execute_modify.start()
        self.execute_modify.return_sig.connect(self.confirm_action_result)

    def confirm_action_result(self, result):
        result = json.loads(result)
        if result['status'] == "OK":
            self.status_shower_callback.setText("Modify student {}'s info success".format(self.stored_name))
        else:
            self.status_shower_callback.setText("Modify student {}'s info fail".format(self.stored_name))
        
        self.init_modify_page()

    def init_modify_page(self):
        self.init_query_info_widget_callback()
        self.radio_button_add.setChecked(False)
        self.radio_button_change.setChecked(False)
        self.combo_box_score.clear()
        self.combo_box_score.update()
        self.change_score_editor.setText("")
        self.add_score_editor.setText("")
        self.add_subject_editor.setText("Subject")

        
