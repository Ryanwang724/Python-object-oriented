from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class DelStu:
    def execute(self, parameters: dict):
        student_id = StudentInfoTable().select_a_student(parameters['name'])
        student_id = student_id[0]
        SubjectInfoTable().delete_a_student(student_id)
        StudentInfoTable().delete_a_student(student_id)

        print(f'    Del {parameters["name"]} success')
        send_msg = {'status': 'OK'}
        return send_msg