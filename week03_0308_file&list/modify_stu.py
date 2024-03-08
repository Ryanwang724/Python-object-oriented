def main(student_list):
    name = input("  Please input a student's name: ")
    for stu in student_list:
        if stu[0] == name:
            new_score = float(input(f"  Please input {name}'s new score: "))
            stu[1] = new_score
            print(f"    Modify [{name}, {new_score}] success")
            return
    print(f"    The name {name} is not found")