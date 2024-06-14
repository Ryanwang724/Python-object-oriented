import tornado.web
from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable


class QueryStudentHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        name = self.get_argument("name")

        stu_id = StudentInfoTable().select_a_student(name)

        if len(stu_id) == 0:
            execution_result = {
                "status": "Fail",
                "reason": "The name is not found."
            }   
        else:
            print("    Query {} success".format(name))            
            execution_result = {
                "status": "OK",
                "scores": SubjectInfoTable().select_student_subject(stu_id[0]) 
            }

        self.write(execution_result)
