def main(student_dict):
    name = input("  Please input a student's name or exit: ")
    if name == "exit":  # 回到主選單
        return
    if name not in student_dict: # 檢查學生是否存在
        print(f"    The name {name} is not found")
        return
    else:
        del student_dict[name]
        print(f"    Del {name} success")