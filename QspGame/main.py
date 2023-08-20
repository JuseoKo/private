import re
import json
from googletrans import Translator
import time

def spacial_text_preprocessing(text_list: list):
    # 러시아 문자 제거
    text_list = [text for text in text_list if not re.search('[а-яА-ЯёЁ]', text)]
    # 일정수 미만 문자 제거
    text_list = [text for text in text_list if len(text) > 10]
    return text_list

def text_word_parser(all_text: str):
    parser_text = re.sub('<img(.*?)\n', '\n', all_text)
    # parser_text = re.sub('=(.*?)\n', '\n', parser_text)
    parser_text = re.sub('<video(.*?)\n', '\n', parser_text)
    parser_text = re.sub('dynamic(.*?)\n', '\n', parser_text)
    parser_text = re.sub('(.*?)\':\n', '\n', parser_text)
    parser_text = re.sub('<TD>(.*?)\n', '\n', parser_text)
    parser_text = re.sub('gt(.*?)\n', '\n', parser_text)
    parser_text = re.sub('gs(.*?)\n', '\n', parser_text)
    parser_text = re.sub('func(.*?)\n', '\n', parser_text)
    parser_text = re.sub('jump(.*?)\n', '\n', parser_text)
    parser_text = re.sub('killvar(.*?)\n', '\n', parser_text, flags=re.IGNORECASE)
    parser_text = re.sub('<font color.*?(?=>)>', '\n', parser_text)
    parser_text = re.sub('if(.*?):', '', parser_text)
    parser_text = re.sub('elseif(.*?):', '', parser_text)
    parser_text = re.sub('\$(.*?)=', '', parser_text)
    # 특정 문자 제거
    parser_text = parser_text.replace('</font>', '').replace('</b>', '').replace('<b>', '').replace('<center>', '').replace('</center>', '').replace('\t', '')
    # 0 . 문장 추출 코드
    # ' ' 사이에 \n가 존재할 경우
    text_list = re.findall('\"(.*?)\"\n', parser_text, re.DOTALL)
    # ================================================
    # 1. 리스트 상태에서 제거해야하는 문자열 제거
    text_list = [s for text in text_list for s in text.split('\n')]
    # text_list = [text.replace('\\', '') for text in text_list]
    text_list = list(set(text_list))
    text_list = spacial_text_preprocessing(text_list=text_list)
    # 2. 글자수로 정렬
    text_list = sorted(text_list, key=len, reverse=True)


    text_dict = {}
    for text in text_list:
        text_dict[text] = google_translator(text)

    with open('./Dict/game_dict.txt', 'w', encoding='utf-16le') as f:
        f.write(str(json.dumps(text_dict, indent=4)))
    print(str(json.dumps(text_dict, indent=4)))
    return text_list


def open_game_text(path: str):
    with open(path, 'r', encoding='utf-16le') as f:
        text_list = text_word_parser(all_text=f.read())


def google_translator(text: str):
    print(f'번역 전 : {text}')
    # 변수 체크 및 저장
    param_check = re.findall('(?P<placeholder>(?:<+|<<)(.*?)(?:>+|>>))', text)
    param_dict = {}
    # 중복제거
    param_check = [param[0] for param in list(set(param_check))]
    # 변수 변환
    for i in range(len(param_check)):
        param_dict[param_check[i]] = 'xazlm' + str(i)
    for k, v in param_dict.items():
        text = text.replace(k, v)
    # 번역
    translated = str(translator.translate(text, src='en', dest='ko').text)

    # 변수 복구
    for k, v in param_dict.items():
        translated = translated.replace(v, k)
        translated = re.sub(v, k, translated, flags=re.IGNORECASE)
    print(f'번역 후 : {translated}')
    time.sleep(0.5)
    return translated


if __name__ == '__main__':
    # 번역 객체 생성
    translator = Translator()
    # google_translator(text=test)
    open_game_text(path='./text.txt')