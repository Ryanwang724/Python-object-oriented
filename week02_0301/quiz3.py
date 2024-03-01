def quiz3():
    while True: 
        layers = int(input("Please enter odd number: "))
        if layers % 2 != 0: # 檢查是否為奇數
            break

    half = layers // 2
    for i in range(half + 1): # 上半部
        print(' '*(half - i)+'*'*(i*2+1))

    for i in range(half ,0,-1): # 下半部
        print(' '*(half + 1 - i)+'*'*(i*2-1))

if __name__ == '__main__':
    quiz3()