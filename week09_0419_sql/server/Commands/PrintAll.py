from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class PrintAll:
    def execute(self, parameters: dict):
        result = {}
        student_id_dict = StudentInfoTable().select_all_student()
        for id, name in student_id_dict.items():
            subject_score_dict = SubjectInfoTable().select_a_student(id)
            result[f'{name}'] = {'name': f'{name}', 'scores': subject_score_dict}

        send_msg = {'status': 'OK', 'parameters': result}
        return send_msg