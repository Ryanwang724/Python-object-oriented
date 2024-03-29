import socket 
import json

from AddStu import AddStu
from PrintAll import PrintAll

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940

action_list = {
    "add": AddStu,  
    "show": PrintAll
}

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))

    def send_command(self, command, parameters):
        send_data = {'command': command, 'parameters': parameters}
        print(f"    The client sent data => {send_data}")
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        self.raw_data = data.decode()
        print(f"    The client received data => {self.raw_data}")

        if self.raw_data == "closing":
            return False
        else:
            self.raw_data = json.loads(self.raw_data) # str to dict
        
        return True
    
    def print_menu(self):
        print()
        print("add: Add a student's name and score")
        print("show: Print all")
        print("exit: Exit")
        selection = input("Please select: ")

        return selection
    
    def main(self):
        keep_going = True
        student_dict = {}
        select_result = "initial"

        while select_result != "exit" and keep_going == True:
            select_result = self.print_menu()
            try:
                para = {}                                       # clear parameters
                if select_result == 'show':                     # show會先送指令至server，再將回傳值印出
                    client.send_command(select_result,{})
                    keep_going = client.wait_response()
                    student_dict = self.raw_data.get('parameters',{})
                    student_dict = PrintAll(student_dict).execute()
                else:                                           # 其餘的是做完處理後才送至Server
                    student_dict = action_list[select_result](student_dict).execute()
                    if bool(student_dict):                      # 確認字典是否有值
                        for key,value in student_dict.items():  # 封裝成Server接受的格式
                            para = {'name':key,'scores':value}
                    client.send_command(select_result, para)
                    keep_going = client.wait_response()
                    if select_result == "add" and self.raw_data['status'] == 'OK': # 提示是否Add成功
                        print(f"    Add {para} success")
                    elif select_result == "add" and self.raw_data['status'] == 'Fail':
                        print(f"    Add {para} fail")

                    student_dict = self.raw_data.get('parameters',{})
            except Exception as e:
                pass

if __name__ == '__main__':
    client = SocketClient(host, port)
    client.main()