str_input = input("enter str: ")
count_dict = {}
for ch in str_input:
    if ch not in count_dict:
        count_dict[ch] = 1
    else:
        count_dict[ch] += 1

print(count_dict)    