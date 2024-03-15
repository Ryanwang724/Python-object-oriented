import add_stu, del_stu, modify_stu, print_all
import pickle

action_list = {
    "add": add_stu.main, 
    "del": del_stu.main, 
    "modify": modify_stu.main, 
    "show": print_all.main
}

def main():
    student_dict = read_student_file()
    select_result = "initial"

    while select_result != "exit":
        select_result = print_menu()
        if select_result == "exit":
            break
        elif select_result not in action_list:
            print("invalid input")
            continue
        try:
            action_list[select_result](student_dict)
        except Exception as e:
            print(e)
    
    restore_student_file(student_dict)

def read_student_file():
    student_dict = dict()
    try:
        with open("student_dict.db", "rb") as fp:
            student_dict = pickle.load(fp)
    except:
        pass

    return student_dict

def restore_student_file(student_dict):
    with open("student_dict.db", "wb") as fp:
        pickle.dump(student_dict, fp)

def print_menu():
    print()
    print("add: add a student's name and score")
    print("del: delete a student")
    print("modify: modify a student's score")
    print("show: print all")
    print("exit: exit")
    selection = input("Please select: ")

    return selection

main()