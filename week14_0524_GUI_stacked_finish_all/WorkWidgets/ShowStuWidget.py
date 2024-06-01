from PyQt6 import QtWidgets, QtGui
from WorkWidgets.WidgetComponents import LabelComponent, ScrollAreaComponent
from SocketClient.ServiceController import ExecuteCommand
import json
import os


class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.this_file_path = os.path.dirname(os.path.abspath(__file__))
        self.background_image_path = os.path.join(self.this_file_path, '..', 'Image', 'background', 'mountain.jpg') # 設定背景圖片
        self.background_pixmap = QtGui.QPixmap(self.background_image_path)
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")

        self.content_displayer = ScrollAreaComponent()
        self.content_displayer.setStyleSheet("""
                                            background-color: transparent;
                                            border: 1px solid black;
                                            """)

        layout.addWidget(header_label, stretch=15)
        layout.addWidget(self.content_displayer, stretch=85)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

    def send_show_command(self):
        self.send_command = ExecuteCommand(command='show', data={})
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_result_show)

    def process_result_show(self, result):
        result = json.loads(result)
        
        text = "==== student list ====\n\n"
        for _ , info in result['parameters'].items():
            for key , value in info.items():
                if key == 'name':
                    text += f"Name: {value}"
                elif key == 'scores':
                    for subject , score in value.items():
                        text += f"      subject: {subject}, score: {score}\n"
                text += "\n"
        text += "=================="
        self.content_displayer.content.setText(text)

    def load(self):
        print('show student')
        self.send_show_command()