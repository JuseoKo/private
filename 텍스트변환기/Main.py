import tkinter as tk
import tkinter.ttk
from tkinter import *
import re
from tkinter import filedialog
from unittest import result
import googletrans
import time

#초기세팅
if True:
    #구글번역기
    translator = googletrans.Translator()
    #사용 데이터
    s_key_data = []
    s_value_data = []
    #사전
    trans_data = {}
    #텍스트 데이터
    data = ""
    #변환된 텍스트 데이터
    change_text = ''
    save_num = 0

#데이터 로드
def data_load():
    #읽기
    data_open = open("./Datas.txt", 'r', encoding="UTF-8")
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
            trans_data[s_key_data[i]] = s_value_data[i]
    return trans_data

data_load()

#텍스트 체인지
def change(trans_data, data):
    #data_load()
    #텍스트 변환
    Value_data = list(trans_data.keys())
    for i in range(0, len(Value_data)):
        Change = trans_data[Value_data[i]]
        data = data.replace(Value_data[i], Change)
    return data


#데이터 입력
def f1_input_data():
    change_text = f1_txt.get('1.0', END)
    f1_txt.delete('1.0', END)
    change_text = change(trans_data, change_text)
    f1_txt1.delete('1.0', END)
    f1_txt1.insert(END, change_text)


#번역문 추가
def f2_input_data():
    global trans_data
    add_text_data = f2_txt.get('1.0', END)
    add_text_data1 = f2_txt1.get('1.0', END)
    f2_txt1.delete('1.0', END)
    f2_txt.delete('1.0', END)   

    add_text_data_l = re.findall('(.+?)\n',str(add_text_data))
    add_text_data1_l = re.findall('(.+?)\n',str(add_text_data1))
    check_l = 0
    
    #번역문 = 원문 확인
    if len(add_text_data_l) > len(add_text_data1_l):
        tkinter.messagebox.showinfo("번역문 초과", "번역문이 원문보다 많습니다.")
    elif len(add_text_data_l) < len(add_text_data1_l):
        tkinter.messagebox.showinfo("번역문 부족", "번역문이 원문보다 적습니다.")    
    elif len(add_text_data_l) == len(add_text_data1_l):
        for i in range(0, len(add_text_data_l)):

            #중복확인 변수
            ch_d = f'\'{add_text_data_l[i].lstrip()}\''
            ch_d_1 = f'\'{add_text_data_l[i].lstrip()}.\''
            ch_d_2 = add_text_data_l[i].strip(".\'""\'")
            ch_d_3 = add_text_data_l[i].strip("\'")
            #번역문 중복확인
            if str(add_text_data_l[i].lstrip()) in trans_data:
                check_l = 1
            # 안녕을 번역문으로 넣었는데 '안녕', '안녕.' 이 존재할 경우 확인
            # '안녕', '안녕.'을 번역문으로 넣었는데 안녕 이 존재할 경우 확인     
            elif ch_d in trans_data:    
                check_l = 1
            elif ch_d_1 in trans_data:      
                check_l = 1 

            # '안녕', '안녕.'을 번역문으로 넣었는데 안녕 이 존재할 경우 확인   
            elif ch_d_2 in trans_data:    
                check_l = 1
            elif ch_d_3 in trans_data:      
                check_l = 1  

            else:    
                data_open = open("./Datas.txt", 'a', encoding="UTF-8")
                datas = f'\n{add_text_data_l[i].lstrip()} @ {add_text_data1_l[i].lstrip()}@'
                data_open.write(datas)    
                trans_data[add_text_data_l[i].lstrip()] = add_text_data1_l[i].lstrip()
        #중복일시 메세지 출력
        if check_l == 1:
            tkinter.messagebox.showinfo("키값 중복", "이미 해당 번역문이 존재합니다.(존재하지 않는 번역문은 정상등록 되었습니다.)")
        else:   
            pass



#문장 추출
def f3_input_data():
    f3_txt1.delete('1.0', END)
    set_text = f3_txt.get('1.0', END)
    f3_txt.delete('1.0', END)
    ex_data = re.sub('<img(.+?)\n', '\n', set_text)

    ex_data = re.sub('<video(.+?)\n', '\n', ex_data)

    ex_data = re.sub('<center>', '', ex_data)
    ex_data = re.sub('</center>', '', ex_data)

    ex_data = re.sub('dynamic(.+?)\n', '\n', ex_data)
    ex_data = re.sub('(.+?)\':\n', '\n', ex_data)

    ex_data = re.sub('dynamic(.+?)\n', '\n', ex_data)

    ex_data = re.sub('<TD>(.+?)\n', '\n', ex_data)

    ex_data = re.sub('gt \'(.+?)\n', '\n', ex_data)

    ex_data = re.sub('gs \'(.+?)\n', '\n', ex_data)

    ex_data = re.sub('if(.+?):','', ex_data)

    ex_data = re.sub('\$(.+?)=', '', ex_data)
    ex_data = re.sub('\t', '', ex_data)
 
    ex_data1 = re.findall('\'(.+?)\'\)\n',ex_data)
    ex_data2 = re.findall('\'(.+?)\'\n',ex_data)

    ex_data = []
    for y in ex_data2:
        #ex_data.append(f'\'{y}\'')
        ex_data.append(y)

    for i in ex_data1:
        ex_data.append(i)

    #gt, gs 검사
    del_list = []
 
    for l in range(0, len(ex_data)):
        try :
            ex_set_d = ex_data[l].find('\', \'')
            if ex_set_d != -1:
                del_list.append(l)
            else: 
                pass    
        except IndexError:
            break    

    for m in range(0, len(del_list)):    
        del ex_data[del_list[m]-m]  


    #ex_data = set(ex_data)
    #ex_data = list(ex_data)
    for i in range(0, len(ex_data)):
        search_data = re.search(' ', ex_data[i])
        #rint(f'타입 : {type(search_data)}\n 데이터 : {search_data}')
        if str(search_data) != 'None':
           # if len(str(ex_data[i])) > 30:
                f3_txt1.insert(END, f'{ex_data[i]}\n')


#P3복사하기(클립보드)
def clipboard():       
    cli_text = f3_txt1.get('1.0', END)
    f3_txt1.delete('1.0', END)
    #win.withdraw()
    win.clipboard_clear()
    win.clipboard_append(cli_text)

#P1복사하기(클립보드)
def clipboard1():       
    cli2_text = f1_txt1.get('1.0', END)
    f1_txt1.delete('1.0', END)
    #win.withdraw()
    win.clipboard_clear()
    win.clipboard_append(cli2_text)

def load_data_key(datas):
    #키 데이터 로드
    s_key_data = []
    key_list = re.findall('(.+?) @', str(datas))
    for i in range(0, len(key_list)):
        strip_data = key_list[i].strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        s_key_data.append(strip_data)
    return s_key_data    

def load_data_value(datas):
    #벨류 데이터 로드
    s_value_data = []
    value_list = re.findall('@ (.+?)@', str(datas))
    for i in range(0, len(value_list)):
        strip_data = value_list[i].strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        s_value_data.append(strip_data)
    return s_value_data

def auto_save():
    sum_d1 = open(f"./datas.txt", 'r', encoding="UTF-8").read()

    sum_d1_key = load_data_key(sum_d1)
    sum_d1_value =load_data_value(sum_d1)


    sum_d2 = open(f"./datas1.txt", 'r', encoding="UTF-8").read()
    sum_d2_key = load_data_key(sum_d2)
    sum_d2_value = load_data_value(sum_d2)

    #리스트 합체
    result_key = sum_d1_key + sum_d2_key
    result_value = sum_d1_value + sum_d2_value

    #정보보관 리스트
    del_value = []
    #최종결과물
    sum_data_k = []

    for z in range(0, len(result_key)):
        if result_key[z] not in sum_data_k:
            #키값 저장
            sum_data_k.append(result_key[z])
        else :
            #삭제번호 저장
            del_value.append(z)

    for x in range(0, len(del_value)):
        del result_value[del_value[x]-x]   

    #저장    
    data_open_auto_save = open(f"./New_data.txt", 'a', encoding="UTF-8")
    for c in range(0, len(sum_data_k)):
        datas = f'{sum_data_k[c]} @ {result_value[c]}@\n'
        data_open_auto_save.write(datas)

def google_tr_data():
    ml = 0
    tr_data_set = ['xy1zx', 'xy2zx', 'xy3zx', 'xy4zx', 'xy5zx', 'xy6zx', 'xy7zx', 'xy8zx']
    tr_data = f2_txt.get('1.0', END)
    tr_data_list = re.findall('(.+?)\n',str(tr_data))

    for o in tr_data_list:
        tr_data_lists = re.findall('<<(.+?)>>', str(o))

        if len(tr_data_lists) == 0:
            tr_data_texts = translator.translate(str(o), dest='ko')
            tr_data_text_last = tr_data_texts.text

        else:
            for c in range(0, len(tr_data_lists)):
                tr_data_text = re.sub('<<(.+?)>>', tr_data_set[c], str(o))
            
            tr_data_texts = translator.translate(tr_data_text, dest='ko')
            
            for b in range(0, len(tr_data_lists)):
                try:
                    tr_data_text_last = re.sub(tr_data_set[b], f'<<{tr_data_lists[b]}>>', str(tr_data_texts.text))
                except IndexError:
                    continue
            tr_data_lists = []    



        ml += 1
        print(f'남은양 : {ml}/{len(tr_data_list)}')
        f2_txt1.insert(END, f'{tr_data_text_last}\n')
        time.sleep(0.35)
    #sats_label = Label(win, text = f'남은작업\n{ml}/{len(tr_data_list)}')
    #sats_label.place(x=400, y=430)
    


#Gui프로그램
if True:
    #gui 초기세팅
    win = tk.Tk()
    win.title("텍스트 변환기")
   # win.geometry('1640x580')

    notebook = tk.ttk.Notebook(win)
    notebook.enable_traversal()
    notebook.pack()
    # 번역 프레임
    if True:
        frame1=Frame(win)
        notebook.add(frame1, text="번역")

        # 번역할 문장
        lable_f1_txt = Label(frame1, text= '번역할 문장 입력')
        lable_f1_txt.pack()
        f1_txt = Text(frame1, width=120, height=14)
        f1_txt.configure(bg='#D3D3D3')
        f1_txt.pack()

        #번역된 문장 출력
        lable_f1_txt1 = Label(frame1, text= '번역된 문장')
        lable_f1_txt1.pack()
        f1_txt1 = Text(frame1, width=120, height=14)
        f1_txt1.configure(bg='#D3D3D3')
        f1_txt1.pack()

        #버튼
        btn = Button(frame1, text='변환하기', command=f1_input_data)
        btn.pack()

        #복사 버튼
        btn = Button(frame1, text='복사하기', command=clipboard1)
        btn.pack()

    #번역 추가
    if True:
        frame2=tkinter.Frame(win)
        notebook.add(frame2, text="번역추가")

        # 번역할 문장
        lable_f2_txt = Label(frame2, text= '원문')
        lable_f2_txt.pack()
        f2_txt = Text(frame2, width=120, height=14)
        f2_txt.configure(bg='#D3D3D3')
        f2_txt.pack()

        #번역된 문장 출력
        lable_f2_txt1 = Label(frame2, text= '번역문')
        lable_f2_txt1.pack()
        f2_txt1 = Text(frame2, width=120, height=14)
        f2_txt1.configure(bg='#D3D3D3')
        f2_txt1.pack()

        #버튼
        btn121 = Button(frame2, text='등록하기', command=f2_input_data)
        btn121.place(x=200, y=430)
        btn232 = Button(frame2, text='구글번역', command=google_tr_data)
        btn232.place(x=600, y=430)

                #유틸기능
    if True:
        frame3=tkinter.Frame(win)
        notebook.add(frame3, text="유틸리티")

        # 문장 추출
        lable_f3_txt = Label(frame3, text= '추출할 문장')
        lable_f3_txt.pack()
        f3_txt = Text(frame3, width=120, height=14)
        f3_txt.insert(END, '데이터 합치기 기능은 datas.txt에 저장되어 있는 데이터를 합치는 기능입니다.\n 이 프로그램과 같은 위치에 하나는 datas.txt , 하나는 datas1.txt 로 이름을 설정하고 버튼을 누르시면 New_datas.txt 파일이 생성됩니다.\n 버그(원문과 문장의 불일치)가 있을 수 있으므로 미리 백업하세요!!')
        f3_txt.configure(bg='#D3D3D3')
        f3_txt.pack()

        #추출된 문장
        lable_f3_txt1 = Label(frame3, text= '추출된 문장')
        lable_f3_txt1.pack()
        f3_txt1 = Text(frame3, width=120, height=14)
        f3_txt1.configure(bg='#D3D3D3')
        f3_txt1.pack()

        #버튼
        btn_f3 = Button(frame3, text='추출하기', command=f3_input_data)
        btn_f3.place(x=200, y=430)
        #btn_f3.pack()
        #자동저장 버튼
        btn_f3_1 = Button(frame3, text = '데이터 합치기', command=auto_save)
        btn_f3_1.place(x=600, y=430)
        #복사버튼
        btn_f3_2 = Button(frame3, text = '복사', command=clipboard)
        btn_f3_2.place(x=400, y=430)


    win.mainloop()