from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class QueryStu:
    def execute(self, parameters:dict):
        student_id = StudentInfoTable().select_a_student(parameters['name'])
        if len(student_id) == 0:
            send_msg = {'status': 'Fail', 'reason': 'The name is not found.'}
        else:
            student_id = student_id[0]
            subject_score_dict = SubjectInfoTable().select_a_student(student_id)
            send_msg = {'status': 'OK', 'scores': subject_score_dict}
            print(f'    Query {parameters["name"]} success')
        return send_msg