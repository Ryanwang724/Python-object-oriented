def main(student_dict):
    temp_dict = {}
    while True:
        name = input("  Please input a student's name or exit: ")
        if name == "exit":  # 回到主選單
            return

        if student_dict.get(name) is not None:  # 檢查學生是否已存在
            print(f"    {name} already exists")
            continue
        else:
            break       

    subject = ""
    while subject != "exit":
        subject = input("  Please input a subject name or exit for ending: ")
        if subject == "exit":
            if bool(temp_dict): # 判斷temp_dict是否為空
                student_dict[name] = temp_dict
            print(f"    Add {name}'s scores successfully")
            break

        if student_dict.get(name) is not None:  # 檢查科目是否已存在
            print(f"    {name} already existed!")
            return

        while True:
            try:
                score = float(input(f"  Please input {name}'s {subject} score or < 0 for discarding the subject: "))
                break
            except Exception as e:
                print(f"    Wrong format with reason {e}, try again")

        if score < 0:
            continue
        else:
            temp_dict[subject] = score