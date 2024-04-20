from SocketClient import SocketClient
from AddStu import AddStu
from DelStu import DelStu
from ModifyStu import ModifyStu
from PrintAll import PrintAll

action_list = {
    "add" : AddStu,
    "del" : DelStu,
    "modify" : ModifyStu,
    "show" : PrintAll
}

host = "127.0.0.1"
port = 20001

class JobDispatcher:
    def job_execute(self, command, socket_client):
        action_list[command](socket_client).execute()


def print_menu():
    print()
    print("add: Add a student's name and score")
    print("del: Delete a student")
    print("modify: Modify a student's score")
    print("show: Print all")
    print("exit: Exit")
    selection = input("Please select: ")

    return selection

def main(socket_client):
    select_result = 'initial'

    while select_result != 'exit':
        select_result = print_menu()
        try:
            JobDispatcher().job_execute(select_result, socket_client)
        except Exception as e:
            pass    

if __name__ == '__main__':
    client = SocketClient(host, port)
    main(client)