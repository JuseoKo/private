import re
import random
if True:
    #사용 데이터
    s_key_data = []
    s_value_data = []
    data = {}
    
#데이터 로드
def data_load():
    #읽기
    data_open = open("./LC.txt", 'r', encoding="UTF-8")
    data_open = data_open.read()
    #키 데이터 로드
    key_list = re.findall('(.+?) @ ', str(data_open))
    for i in range(0, len(key_list)):
        strip_data = key_list[i].strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        s_key_data.append(strip_data)

    #벨류 데이터 로드
    value_list = re.findall('@ (.+?)@', str(data_open))
    for i in range(0, len(value_list)):
        strip_data = value_list[i].strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        s_value_data.append(strip_data)
    #딕셔너리에 로드
    for i in range(0, len(s_key_data)):
            # (f'수 : {len(s_value_data[i])}\n 역수 : {len(s_key_data)}')
            data[s_key_data[i]] = s_value_data[i]
    return data


if __name__ == '__main__':
    data_load()
    x = list(data.keys())
    y = list(data.values())
    while True:
        z = random.randrange(0, len(x))
        print(f'-----------------남은단어 : {len(x)}')
        input(f'{x[z]}')
        a = input(f'{y[z]}')
        if a == 'q':
            break
        elif a == '\'':
            del x[z], y[z]
    #종료 = q , 외움처리 = a
    #C:\Users\maria\Desktop\Code

    

