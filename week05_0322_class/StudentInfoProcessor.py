import pickle
class StudentInfoProcessor:
    def __init__(self):
        self.stu_dict = dict()
    def read_student_file(self):
        try:
            with open("student_dict.db", "rb") as fp:
                self.stu_dict = pickle.load(fp)
        except:
            pass
        return self.stu_dict
    def restore_student_file(self,input_dict):
        with open("student_dict.db", "wb") as fp:
            pickle.dump(input_dict, fp)