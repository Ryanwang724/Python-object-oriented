def main(student_list):
    name = input("  Please input a student's name: ")
    for stu in student_list:
        if stu[0] == name:
            student_list.remove(stu)
            print(f"    Del {name} success")
            return
    print(f"    The name {name} is not found")