import requests
import re
import sys
from tqdm import tqdm

def get_date(page:int) -> tuple[list, list]:
    data = []
    file = []
    headers = requests.utils.default_headers()
    headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)
    for i in tqdm(range(1, page+1), ncols=50):
        url = f'https://exam.naer.edu.tw/searchResult.php?page={i}&orderBy=lastest&keyword=&selCountry=&selCategory=0&selTech=0&selYear=&selTerm=&selType=&selPublisher='
        res = requests.get(url, headers=headers)

        data += re.findall(r'<td bgcolor="#FFFFFF" class="t4">([^<]*)</td>', res.text)
        file += re.findall(
            r'<a href="(/(?:otc)[^"]*)" target="_blank"><img border=0 src="/theme/default/sys/download.png" />'
            r'|(?=<td bgcolor="#FFFFFF" class="t4"><img border=0 src="/theme/default/sys/download-no.png" /></td><td bgcolor="#FFFFFF" class="t4"><a href="/base/otc/testStoreFile/)',
            res.text
        )

    return data, file

def statistics_data(data:list, file:list, field:int) -> tuple[dict, dict]:
    result_dict = {}
    statistics_dict = {}

    statistics_version = {}
    statistics_subject = {}
    statistics_school = {}

    for i in range(len(data)//field):
        temp_dict = {}
        temp_dict['city'] = data[field*i].strip()
        temp_dict['school'] = data[field*i+1].strip()
        temp_dict['grade'] = data[field*i+2].strip()
        temp_dict['semester'] = data[field*i+3].strip()
        temp_dict['field'] = data[field*i+4].strip()
        temp_dict['subject'] = data[field*i+5].strip()
        temp_dict['type'] = data[field*i+6].strip()
        temp_dict['version'] = data[field*i+7].strip()
        temp_dict['CTR'] = int(data[field*i+8].replace(',','').strip())
        temp_dict['file'] = file[i].strip()
        result_dict[i] = temp_dict

        statistics_version[temp_dict['version']] = statistics_version.get(temp_dict['version'], 0) + 1
        statistics_subject[temp_dict['subject']] = statistics_subject.get(temp_dict['subject'], 0) + 1
        statistics_school[temp_dict['school']] = statistics_school.get(temp_dict['school'], 0) + 1
    
    statistics_version = {k: v for k, v in sorted(statistics_version.items(), key=lambda item: item[1], reverse=True)}
    statistics_subject = {k: v for k, v in sorted(statistics_subject.items(), key=lambda item: item[1], reverse=True)}
    statistics_school = {k: v for k, v in sorted(statistics_school.items(), key=lambda item: item[1], reverse=True)}

    statistics_dict['version'] = statistics_version
    statistics_dict['subject'] = statistics_subject
    statistics_dict['school'] = statistics_school

    return result_dict, statistics_dict

def process_total_result(result_dict:dict, mode:str):
    if mode == 'show':
        FILE = sys.stdout
    elif mode == 'save':
        f = open('analysis_result_hw2.txt','w', encoding='utf-8')
        FILE = f

    for cnt, info in result_dict.items():
        for k,v in info.items():
            print(f'{v}',end=' ', file=FILE)
        print('',end='\n', file=FILE)

    if mode == 'save':
        f.close()

def print_dict(data:dict):
    print_str = ''
    for k,v in data.items():
        print_str += f'{k}: {v}, '
    print_str = print_str[:-2]
    print(print_str)

if __name__ == '__main__':
    PAGE = 1910    # 欲下載的頁數
    data, file = get_date(PAGE)

    FIELD = 10     # 欄位數量
    result_dict, statistics_dict = statistics_data(data, file, FIELD)

    process_total_result(result_dict, 'show') # 在終端機顯示出結果
    process_total_result(result_dict, 'save') # 將結果存入txt

    print(f'\n出版社題庫數量統計: ',end='') 
    print_dict(statistics_dict['version'])  # 印出各出版社統計數量
    print(f'\n各科目題庫數量統計: ',end='')
    print_dict(statistics_dict['subject'])  # 印出各科目統計數量
    print(f'\n各學校題庫數量統計: ',end='')
    print_dict(statistics_dict['school'])   # 印出各學校統計數量