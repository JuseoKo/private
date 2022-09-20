import random
import json

if True:
    path = './data.json'

#json 오픈기능
def json_load():
    #json 오픈
    with open(path, encoding='utf-8') as f:
        jsons = json.load(f)

    return jsons

#데이터 추가기능
def data_add(add_eg_data, add_change_data):
    Data["Data"][add_eg_data] = add_change_data
    with open(path, 'w') as f:
        json.dump(Data, f, ensure_ascii=False, indent=3)

if __name__ == '__main__':
    # 데이터 파일 로드
    Data = json_load()
    ch = input('데이터 등록 : 0 \n학습 : 1 \n 입력 : ')
    if ch == 1:
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
    else :
        while True:
            inp = input('단어 입력 : ')
            inp_rs = input('뜻 입력 : ')
            if inp == 'q':
                break
            else :
                data_add(inp, inp_rs)

        #종료 = q , 외움처리 = a
    

