from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class AddStu:
    def execute(self, parameters: dict):
        StudentInfoTable().insert_a_student(parameters['name'])
        student_id = StudentInfoTable().select_a_student(parameters['name'])
        student_id = student_id[0]
        for subject, score in parameters['scores'].items():
            SubjectInfoTable().insert_a_student(student_id, subject, score)

        send_msg = {'status': 'OK'}
        return send_msg