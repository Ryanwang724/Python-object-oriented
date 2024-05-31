from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, TextBrowserComponent
from SocketClient.ServiceController import ExecuteCommand
import json
import os


class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.this_file_path = os.path.dirname(os.path.abspath(__file__))
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")
        self.text_browser = TextBrowserComponent()

        # background_image_path = os.path.join(self.this_file_path, '..', 'Image', 'background', 'pink.jpg')

        # if os.path.exists(background_image_path):
        #     # 使用正確的路徑格式
        #     background_image_path = background_image_path.replace('\\', '/')
        #     self.setStyleSheet(f'background-image: url("{background_image_path}");')
        # else:
        #     print(f"Error: The background image {background_image_path} does not exist.")

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