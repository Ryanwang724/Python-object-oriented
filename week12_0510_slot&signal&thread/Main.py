from WorkWidgets.MainWidget import MainWidget
from PyQt6.QtWidgets import QApplication
import sys
from SocketClient.SocketClient import SocketClient

app = QApplication([])
client = SocketClient(host='127.0.0.1', port=20001)
main_window = MainWidget(client)

main_window.setFixedSize(700, 400)
main_window.show()
# main_window.showFullScreen()

sys.exit(app.exec())