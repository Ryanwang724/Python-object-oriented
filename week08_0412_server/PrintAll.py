class PrintAll:
    def __init__(self,stu_dict,input_dict):
        self.stu_dict = stu_dict                                  # server端內部管理資料
        self.result_dict = {'status' : '', 'parameters' : dict()} # 回傳結果格式

    def execute(self):
        self.result_dict['parameters'] = self.stu_dict            # 維護回傳結果
        self.result_dict['status'] = 'OK'
        return self.stu_dict, self.result_dict