from DBController.DBConnection import DBConnection


class StudentInfoTable:
    def insert_a_student(self, name):
        command = "INSERT INTO student_info (name) VALUES  ('{}');".format(name)
            
        send_command_to_DB(command)

    def select_a_student(self, name):
        command = "SELECT * FROM student_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['stu_id'] for row in record_from_db]

    def delete_a_student(self, stu_id):
        command = "DELETE FROM student_info WHERE stu_id='{}';".format(stu_id)

        send_command_to_DB(command)

    def update_a_student(self, stu_id, name):
        command = "UPDATE student_info SET name='{}' WHERE stu_id='{}';".format(name, stu_id)

        send_command_to_DB(command)

    def select_all_student(self):
        command = "SELECT * FROM student_info ;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        student_id_dict = {}
        for stu in record_from_db:
            student_id_dict[stu[0]] = stu[1]
        return student_id_dict

def send_command_to_DB(command):
    with DBConnection() as connection:
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()