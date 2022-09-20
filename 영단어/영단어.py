import random
import json

#json 오픈기능
def json_load():
    #json 오픈
    with open('data.json', encoding='utf-8') as f:
        jsons = json.load(f)
    return jsons

#데이터 추가기능
def data_add(add_eg_data, add_change_data):
    Data["Data"][add_eg_data] = add_change_data
    print(Data["Data"])

if __name__ == '__main__':
    # 데이터 파일 로드
    Data = json_load()
    x = list(Data['Data'].keys())
    y = list(Data['Data'].values())
    #입력받기, 파일전송 or 데이터 입력중 택1
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

    

