from SocketClient import SocketClient

class ModifyStu:
    def __init__(self, socket_client: SocketClient):
        self.socket_client = socket_client
        self.subject_list = []

    def input_stu_name(self):
        name = input("  Please input a student's name: ")
        command = 'query'
        parameters = {'name': f'{name}'}
        self.socket_client.send_command(command, parameters)
        receive_data = self.socket_client.wait_response()
        if receive_data['status'] == 'OK':
            self.print_subject(receive_data['scores'])
            return name, receive_data['scores']
        elif receive_data['status'] == 'Fail':
            print(f'    The name {name} is not found')
            return None, None

    def print_subject(self, scores: dict):
        for subj, _ in scores.items():
            self.subject_list.append(subj)
            print_result = ' '.join(self.subject_list)
        print(f"Current subjects are {print_result}\n")

    def input_subject(self, name: str, score: dict):
        change_subject = input("  Please input a subject you want to change: ")
        exist = False
        try:
            if change_subject not in self.subject_list:   # 檢查科目是否存在
                change_score = float(input(f"  Add a new subject for {name} please input {change_subject} score or < 0 for discarding the subject: "))
            else:                                         # 如果科目存在
                change_score = float(input(f"  Please input {change_subject}'s new score of {name}: "))
                exist = True
        except Exception as e:
            print(e)
        else:
            if change_score < 0:
                return
            else:
                score[f'{change_subject}'] = change_score
                command = 'modify'
                parameters = {'name': f'{name}', 'scores_dict': score}
                self.socket_client.send_command(command, parameters)
                receive_data = self.socket_client.wait_response()

                if receive_data['status'] == 'OK' and exist == False:
                    print(f"  Add [{name}, {change_subject}, {change_score}] success")
                elif receive_data['status'] == 'OK' and exist == True:
                    print(f"    Modify [{name}, {change_subject}, {change_score}] success")

    def execute(self):
        name, score = self.input_stu_name()
        if name is not None and score is not None:
            self.input_subject(name, score)