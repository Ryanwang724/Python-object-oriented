from SocketClient import SocketClient

class PrintAll:
    def __init__(self, socket_client: SocketClient):
        self.socket_client = socket_client

    def execute(self):
        command = 'show'
        parameters = {}
        self.socket_client.send_command(command, parameters)
        receive_data = self.socket_client.wait_response()
        print ("\n==== student list ====")
        for _ , info in receive_data['parameters'].items():
            for key , value in info.items():
                if key == 'name':
                    print(f"\nName: {value}")
                elif key == 'scores':
                    for subject , score in value.items():
                        print(f"  subject: {subject}, score: {score}")
        print ("\n======================")