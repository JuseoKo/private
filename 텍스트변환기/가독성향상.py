import re

if True:
    data = []
    change_data = []
    change_add = '\'&\'\"'
    key_data = []

def mains():
    data_open = open("./test.txt", 'r', encoding="UTF-8")
    data_open = data_open.read()

    #변경할 데이터 로드
    add_data = re.findall('@ (.+?)@', str(data_open))
    for i in range(0, len(add_data)):
        strip_data = add_data[i].strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        data.append(strip_data)

    #저장할때 필요한 데이터 로드
    key_list = re.findall('(.+?) @ ', str(data_open))
    for i in range(0, len(key_list)):
        strip_data = key_list[i].strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        key_data.append(strip_data)

    for j in data:
        add = re.sub(' "', change_add, j)
        change_data.append(add)

    #다시저장
    data_open_auto_save = open(f"./New_data.txt", 'a', encoding="UTF-8")
    for c in range(0, len(key_data)):
        datas = f'{key_data[c]} @ {change_data[c]}@\n'
        data_open_auto_save.write(datas)


if __name__ == '__main__':
    mains()
    print('완료')