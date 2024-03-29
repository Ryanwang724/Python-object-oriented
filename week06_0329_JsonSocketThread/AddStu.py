class AddStu:
    def __init__(self,input_dict):
        self.stu_dict = input_dict

    def input_sub(self,name):
        temp_dict = {}
        subject = ""
        while subject != "exit":
            subject = input("  Please input a subject name or exit for ending: ")
            if subject == "exit":
                if bool(temp_dict): # 判斷temp_dict是否有資料
                    self.stu_dict[name] = temp_dict
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
                temp_dict[subject] = score

    def input_stu_name(self):
        while True:
            name = input("  Please input a student's name or exit: ")
            if name == "exit":  # 回到主選單
                return self.stu_dict
            else:
                break
        self.input_sub(name)

    def execute(self):
        self.input_stu_name() # 輸入學生姓名
        return self.stu_dict