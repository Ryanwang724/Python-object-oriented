from threading import Thread
import socket
import json

from AddStu import AddStu
from PrintAll import PrintAll
from StudentInfoProcessor import StudentInfoProcessor

host = "127.0.0.1"
port = 20001

action_list = {
    "add": AddStu,  
    "show": PrintAll
}

class SocketServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.stu_dict = dict()        # server端資料存放處

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            print("{} connected".format(address))
            self.new_connection(connection=connection,
                                address=address)

    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={
                   "connection": connection,
                   "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except Exception as e:
                print("Exception happened {}, {}".format(e, address))
                keep_going = False
            else:
                if not message:
                    keep_going = False
                    break
                message = json.loads(message)
                if message['command'] == "close":
                    connection.send("closing".encode())
                    keep_going = False
                else:
                    print(message)
                    try:
                        self.stu_dict, result_dict = action_list[message['command']](self.stu_dict, message['parameters']).execute()
                    except Exception as e:
                        pass
                    print(f'    server received: {message} from {address}')
                    connection.send(json.dumps(result_dict).encode())                   # 將執行結果回傳至client
        
        connection.close()
        print("{} close connection".format(address))


if __name__ == '__main__':
    server = SocketServer(host, port)
    server.daemon = True
    server.serve()

    server.stu_dict = StudentInfoProcessor().read_student_file()  # 讀取db檔

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    StudentInfoProcessor().restore_student_file(server.stu_dict)  # 存db檔
    print("leaving ....... ")
    server.server_socket.close()