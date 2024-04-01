class AddStu:
    def __init__(self,input_dict):
        self.stu_dict = input_dict

    def input_sub(self,name):
        temp_dict = {}
        subject = ""
        while subject != "exit":
            subject = input("  Please input a subject name or exit for ending: ")
            if subject == "exit":
                if bool(temp_dict):                 # 判斷temp_dict是否有資料 空:False 非空:True
                    self.stu_dict[name] = temp_dict # 有資料才存
                break

            while True:
                try:
                    score = float(input(f"  Please input {name}'s {subject} score or < 0 for discarding the subject: "))
                    break
                except Exception as e:
                    print(f"    Wrong format with reason {e}, try again")

            if score < 0:    # score <  0 ------> discard
                continue
            else:            # score >= 0 ------> save to temp_dict
                temp_dict[subject] = score

    def input_stu_name(self):
        while True:             # 輸入的名字不為"exit"才跳出while loop
            name = input("  Please input a student's name or exit: ")
            if name == "exit":  # 回到主選單
                return self.stu_dict
            else:
                break
        self.input_sub(name)    # 進入輸入科目環節

    def execute(self):
        self.input_stu_name()   # 輸入學生姓名開始
        return self.stu_dict