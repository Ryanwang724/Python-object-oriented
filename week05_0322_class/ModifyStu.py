class ModifyStu:
    def __init__(self,input_dict):
        self.stu_dict = input_dict
    def print_sub(self,name):
        temp_sub_str=""   # 存取所有科目名稱
        for su,sc in self.stu_dict[name].items():
            temp_sub_str += su +" "
        print(f"Current subjects are {temp_sub_str}\n")
    def input_sub(self,name):
        change_subject = input("  Please input a subject you want to change: ")
        if change_subject not in self.stu_dict[name]:   # 檢查科目是否存在
            try:
                change_score = float(input(f"  Add a new subject for {name} please input {change_subject} score or < 0 for discarding the subject: "))
                if change_score < 0:
                    return self.stu_dict
                else:
                    self.stu_dict[name][change_subject] = change_score
                    print("  Add successfully")
            except Exception as e:
                print(e)
        else:  # 如果科目存在
            try:
                change_score = float(input(f"  Please input {change_subject}'s new score of {name}: "))
                if change_score < 0:
                    return self.stu_dict
                else:
                    self.stu_dict[name][change_subject] = change_score
                    print(f"    Modify [{name}, {change_subject}, {change_score}] success")
            except Exception as e:
                print(e)
    def input_stu_name(self):
        name = input("  Please input a student's name or exit: ")
        if name not in self.stu_dict: # 檢查學生是否存在
            print(f"    The name {name} is not found")
            return self.stu_dict
        self.print_sub(name)
        self.input_sub(name)
    
    def execute(self):
        self.input_stu_name()
        return self.stu_dict