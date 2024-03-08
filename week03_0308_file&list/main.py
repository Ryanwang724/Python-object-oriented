import add_stu, del_stu, modify_stu, print_all

def main():
    ## NOTE: NO if else elif judgements are allowed in the main function !!!!
    student_list = read_student_file()
    select_result = 0
    func_mapping = {  # function dictionary
        0 : add_stu.main,
        1 : del_stu.main,
        2 : modify_stu.main,
        3 : print_all.main,
    }

    while select_result != 4 :
        # call main functions in add_stu, del_stu, modify_stu, print_all here
        try:
            select_result = print_menu()
            if select_result == 4:
                break
            result = func_mapping[select_result](student_list)
        except KeyError:
            print(f"Wrong input range! Your input:{select_result}")
        except Exception as e:
            print(f"The exception [{e}] occur.")

    restore_student_file(student_list)

def read_student_file():
    student_list = list()
    try:
        with open("student_list.txt", "r") as fp:
            for line in fp:
                if len(line) > 0:
                    line = line.rstrip("\n").split(":")
                    student_list.append([line[0], float(line[1])])
    except:
        pass

    return student_list

def restore_student_file(student_list):
    # restore student list to file here
    with open('student_list.txt', 'w') as f:
        for stu in student_list:
            f.write(f"{stu[0]}:{stu[1]}\n")

def print_menu():
    print()
    print("0. Add a student's name and score")
    print("1. Delete a student")
    print("2. Modify a student's score")
    print("3. Print all")
    print("4. Exit")
    selection = int(input("Please select: "))

    return selection

main()