car  = input("請輸入6碼車牌:")

if car[0].isalpha() or car[1].isalpha():
    newCar = car[2:] + car[:2]
elif car[4].isalpha() or car[5].isalpha():
    newCar = car[4:] + car[:4]

print(f"原始:{car}, 修改後:{newCar}")