def quiz5():
    def guessing(start,end,limit):
        import random
        answer = random.randint(start,end)
        for i in range(limit):
            while True:
                guess = int(input(f"Please guess a number from {start} to {end}: "))
                if guess >= start and guess <= end:
                    break
                else:
                    print("Invalid input")
            if guess == answer:
                return "You passed"
            elif guess > answer:
                end = guess
            elif guess < answer:
                start = guess

        return "Achieve limitted"

    def main(): 
        limit = 6
        start = 0
        end = 100
        result = guessing(start = start,end = end,limit = limit)
        print(result) 
    
    main()

if __name__ == '__main__':
    quiz5()