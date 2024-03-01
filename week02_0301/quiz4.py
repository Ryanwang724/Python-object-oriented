def quiz4():
    rows = int(input("Number of rows: "))
    columns = int(input("Number of columns: "))
    grid = int(input("Grid size: "))

    for i in range(rows):
        print(('+' + grid * '-') * columns + '+')
        for j in range(grid):
            print(('|' + grid * ' ') * columns + '|')
    print(('+' + grid * '-') * columns + '+')        

if __name__ == '__main__':
    quiz4()    