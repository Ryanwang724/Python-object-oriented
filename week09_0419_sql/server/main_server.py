from Commands.AddStu import AddStu
from Commands.QueryStu import QueryStu
from Commands.DelStu import DelStu
from Commands.ModifyStu import ModifyStu
from Commands.PrintAll import PrintAll
from SocketServer.SocketServer import SocketServer
from DBController.DBConnection  import DBConnection
from DBController.DBInitializer import DBInitializer

action_list = {
    "add" : AddStu,
    "query" : QueryStu,
    "delete" : DelStu,
    "modify" : ModifyStu,
    "show" : PrintAll
}

host = "127.0.0.1"
port = 20001

class JobDispatcher:
    def job_execute(self, command, parameters):
        execute_result = action_list[command]().execute(parameters)
        return execute_result

def main():
    DBConnection.db_file_path = "database.db"
    DBInitializer().execute()

    job_dispatcher = JobDispatcher()
    server = SocketServer(host, port, job_dispatcher)
    server.daemon = True
    server.serve()

    while True:
        command = input()
        if command == "finish":
            break

    print("leaving ....... ")
    server.server_socket.close()

if __name__ == "__main__":
    main()