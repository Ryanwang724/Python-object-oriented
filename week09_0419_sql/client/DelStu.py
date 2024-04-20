from SocketClient import SocketClient

class DelStu:
    def __init__(self, socket_client: SocketClient):
        self.socket_client = socket_client

    def execute(self):
        name = input("  Please input a student's name: ")
        command = 'query'
        parameters = {'name': f'{name}'}
        self.socket_client.send_command(command, parameters)
        receive_data = self.socket_client.wait_response()

        if receive_data['status'] == 'OK':
            confirm = input("  Confirm to delete (y/n): ")
            if confirm.lower() == 'y':
                command = 'delete'
                parameters = {'name': f'{name}'}
                self.socket_client.send_command(command, parameters)
                receive_data = self.socket_client.wait_response()
                if receive_data['status'] == 'OK':
                    print('    Delete success')
            elif confirm.lower() == 'n':
                pass
            else:
                print('wrong input!')

        elif receive_data['status'] == 'Fail':
            print(f'    The name {name} is not found')