class AddStu:
    def __init__(self,stu_dict,input_dict):
        self.stu_dict = stu_dict                                  # server端內部管理資料
        self.input_dict = input_dict                              # client端送入之指令
        self.result_dict = {'status': '','reason': ''}            # 回傳結果格式

    def check_receive_data(self):
        if self.input_dict.get('name') in self.stu_dict:          # 檢查學生是否已存在
            self.result_dict['status'] = 'Fail'                   # 若已存在=>維護回傳結果
            self.result_dict['reason'] = 'The name already exists.'
            return True
        else:
            return False

    def maintain_stu_dict(self):                                  # 維護server端儲存的資料
        self.stu_dict[self.input_dict['name']] = self.input_dict  # 新增一筆key/value對並存成server端儲存格式
        self.result_dict['status'] = 'OK'                         # 維護回傳結果
        self.result_dict.pop('reason')                            # 若新增成功=>不需傳reason

    def execute(self):
        already_exist = self.check_receive_data()                 # 檢查name是否重複
        if already_exist == False:                                # 不重複才維護
            self.maintain_stu_dict()
        return self.stu_dict, self.result_dict