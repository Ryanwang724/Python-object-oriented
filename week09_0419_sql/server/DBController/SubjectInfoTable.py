from DBController.DBConnection import DBConnection


class SubjectInfoTable:
    def insert_a_student(self, stu_id, subject, score):
        command = f"INSERT INTO subject_info (stu_id, subject, score) VALUES  ('{stu_id}', '{subject}', '{score}');"
            
        send_command_to_DB(command)

    def select_a_student(self, stu_id):
        command = f"SELECT * FROM subject_info WHERE stu_id='{stu_id}';"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        subject_score_dict = {}
        for row in record_from_db:
            subject = row['subject']
            score = row['score']
            subject_score_dict[subject] = score
    
        return subject_score_dict

    def delete_a_student(self, stu_id):
        command = f"DELETE FROM subject_info WHERE stu_id='{stu_id}';"

        send_command_to_DB(command)

    def update_a_student(self, stu_id, subject, score):
        command = f"UPDATE subject_info SET score = '{score}' WHERE stu_id='{stu_id}' AND subject='{subject}';"

        send_command_to_DB(command)

def send_command_to_DB(command):
    with DBConnection() as connection:
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()