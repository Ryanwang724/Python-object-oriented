import re
import sys

def get_data(file:str) -> tuple[dict, dict]:
    with open(file, 'r') as f:
        data = f.readlines()

    result_dict = {}
    total_cnt_dict = {}
    for line in data:
        info_dict = {}
        object_dict = {}

        # 取出需要的字串
        obj = re.findall(r'buys (\S+) for', line)
        price = re.findall(r'\$([0-9]+)', line)
        name = re.findall(r'(\S+) buys', line)
        identity = re.findall(r'(\[VIP\]) ', line)

        # 對取出的資料作處理
        name = ''.join(name)
        obj = ''.join(obj)
        price = int(''.join(price))
        identity = ''.join(identity)

        # 統計各物品的總銷售額
        total_cnt_dict[obj] = total_cnt_dict.get(obj, 0) + price

        object_dict[obj] = price
        
        info_dict['name'] = name
        if identity == '[VIP]':
            info_dict['identity'] = 'VIP'
        else:
            info_dict['identity'] = 'Normal'
        info_dict['object'] = object_dict
        
        # 更新result_dict
        if name not in result_dict:
            result_dict[name] = info_dict
        else:
            compare_dict = result_dict.get(name)
            if obj in compare_dict['object']:
                compare_dict['object'][obj] += price
            else:
                compare_dict['object'].update(object_dict)
            result_dict[name] = compare_dict

    # 排序
    for name, info in result_dict.items():
        info['object'] = {k: v for k, v in sorted(info['object'].items(), key=lambda item: item[0])}
    total_cnt_dict = {k: v for k, v in sorted(total_cnt_dict.items(), key=lambda item: item[0])}

    return result_dict, total_cnt_dict

def process_data(result_dict:dict, total_cnt_dict:dict, mode:str):
    if mode == 'show':
        FILE = sys.stdout
    elif mode == 'save':
        f = open('analysis_result_hw1.txt','w')
        FILE = f

    print('[VIP]', file=FILE)
    for name, info in result_dict.items():
        if info['identity'] == 'VIP':
            obj_str = ''
            for obj, price in info['object'].items():
                obj_str += f'{obj}: ${price}, '
            obj_str = obj_str[:-2] # 去除最後的', '
            print(f"{info['name']} buys {obj_str}", file=FILE)

    print('\n[Member]', file=FILE)
    for name, info in result_dict.items():
        if info['identity'] == 'Normal':
            obj_str = ''
            for obj, price in info['object'].items():
                obj_str += f'{obj}: ${price}, '
            obj_str = obj_str[:-2] # 去除最後的', '
            print(f"{info['name']} buys {obj_str}", file=FILE)
    
    print('', file=FILE)
    for obj, price in total_cnt_dict.items():
        print(f'Total {obj} sales: ${price}', file=FILE)

    if mode == 'save':
        f.close()


if __name__ == '__main__':
    input_file = 'log.txt'
    result_dict, total_cnt_dict = get_data(input_file)
    process_data(result_dict, total_cnt_dict, 'show') # 在終端機顯示出結果
    process_data(result_dict, total_cnt_dict, 'save') # 將結果存入txt