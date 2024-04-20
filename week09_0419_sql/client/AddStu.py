from SocketClient import SocketClient


class AddStu:
    def __init__(self, socket_client: SocketClient):
        self.socket_client = socket_client

    def input_subject(self, name: str):
        score_dict = {}
        subject = ""
        while subject != "exit":
            subject = input("  Please input a subject name or exit for ending: ")
            if subject == "exit":
                if bool(score_dict): # 判斷score_dict是否有資料
                    # socket 送出
                    command = 'add'
                    parameters = {'name': f'{name}', 'scores': score_dict}
                    self.socket_client.send_command(command, parameters)
                    receive_data = self.socket_client.wait_response()
                    if receive_data['status'] == 'OK':
                        print(f'    Add {parameters} success')
                break

            while True:
                try:
                    score = float(input(f"  Please input {name}'s {subject} score or < 0 for discarding the subject: "))
                    break
                except Exception as e:
                    print(f"    Wrong format with reason {e}, try again")

            if score < 0:
                continue
            else:
                score_dict[subject] = score

    def input_stu_name(self):
        name = input("  Please input a student's name: ")
        command = 'query'
        parameters = {'name': f'{name}'}
        self.socket_client.send_command(command, parameters)
        receive_data = self.socket_client.wait_response()
        if receive_data['status'] == 'Fail':
            # 執行後續add
            self.input_subject(name)

    def execute(self):
        self.input_stu_name() # 輸入學生姓名