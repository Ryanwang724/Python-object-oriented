from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
import json
from SocketClient.SocketClient import SocketClient


class ServiceController:
    socket_client = SocketClient(host='127.0.0.1', port=20001)

    def command_sender(self, command, data):
        self.socket_client.send_command(command, data)
        result = self.socket_client.wait_response()
        return result

class ExecuteCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, command, data):
        super().__init__()
        self.command = command
        self.data = data

    def run(self):
        result = ServiceController().command_sender(self.command, self.data)
        self.return_sig.emit(json.dumps(result))
