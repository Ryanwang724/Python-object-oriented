def main(student_list):
    name = input("  Please input a student's name: ")
    score = float(input(f"  Please input {name}'s score: "))

    for stu in student_list:  # 檢查是否學生已存在
        if stu[0] == name:
            print(f"    {name} already existed!")
            return
    student_list.append([name, score])
    print(f"    Add [{name}, {score}] success")