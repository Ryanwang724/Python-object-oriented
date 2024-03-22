class DelStu:
    def __init__(self,input_dict):
        self.stu_dict = input_dict
    def execute(self):
        name = input("  Please input a student's name or exit: ")
        if name == "exit":  # 回到主選單
            return self.stu_dict
        if name not in self.stu_dict: # 檢查學生是否存在
            print(f"    The name {name} is not found")
            return self.stu_dict
        else:
            del self.stu_dict[name]
            print(f"    Del {name} success")
        return self.stu_dict