def quiz1():
    layers = int(input("Please enter a value: "))

    for i in range(layers,0,-1): # 上半部
        print('*'*i)
    for i in range(2,layers + 1): # 下半部
        print('*'*i)

if __name__ == '__main__':
    quiz1()