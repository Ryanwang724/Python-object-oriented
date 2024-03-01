import quiz1, quiz2, quiz3, quiz4, quiz5

def menu():
    print("1. Print double triangle")
    print("2. Print spacing triangle")
    print("3. Print diamond")
    print("4. Print grid")
    print("5. Guessing game")

def main():
    keep_going = "y"
    while keep_going == "y":
        print('\n')
        menu()
        select = int(input("Please select: "))
        if select == 1:
            quiz1.quiz1()
        elif select == 2:
            quiz2.quiz2()
        elif select == 3:
            quiz3.quiz3()
        elif select == 4:
            quiz4.quiz4()
        elif select == 5:
            quiz5.quiz5()
        else:
            print("Invalid input")
        print('\n')    
        keep_going = input("Test again (y)? ")

if __name__ == '__main__':
    main()