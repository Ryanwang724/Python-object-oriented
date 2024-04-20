from threading import Thread
import socket
import json

host = "127.0.0.1"
port = 20001

class SocketServer(Thread):
    def __init__(self, host, port, job_dispatcher):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.job_dispatcher = job_dispatcher

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
                    print(f'    server received: {message} from {address}')
                    try:
                        result = self.job_dispatcher.job_execute(message['command'], message['parameters'])
                    except Exception as e:
                        print(e)
                    else:
                        connection.send(json.dumps(result).encode())
        

        print("{} close connection".format(address))
        connection.close()


if __name__ == '__main__':
    server = SocketServer(host, port)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    print("leaving ....... ")
    server.server_socket.close()