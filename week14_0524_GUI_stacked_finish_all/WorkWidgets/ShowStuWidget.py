from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, TextBrowserComponent
from SocketClient.ServiceController import ExecuteCommand
import json


class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")
        self.text_browser = TextBrowserComponent()

        layout.addWidget(header_label, stretch=15)
        layout.addWidget(self.text_browser, stretch=85)
        self.setLayout(layout)

    def send_show_command(self):
        self.send_command = ExecuteCommand(command='show', data={})
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_result_show)
    
    def process_result_show(self, result):
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

    def load(self):
        print('show student')
        self.send_show_command()