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
    # if \n
    parser_text = re.sub('if (.*?)\n', '\n', parser_text)
    parser_text = re.sub('=iif(.*?),', '\n', parser_text)
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
    return text_list

def translator_run(text_list: list):
    # 번역
    text_dict = {}
    for text in text_list:
        trans_check = 1
        while trans_check == 1:
            try:
                text_dict[text] = trans_from(text)
            except:
                time.sleep(10)
                text_dict[text] = trans_from(text)
            trans_check = 0
    #저장
    with open('./Dict/game_dict.py', 'w', encoding='utf-8') as f:
        f.write('trans_dict = '+str(json.dumps(text_dict, indent=4, ensure_ascii=False)))
    return None

def trans_from(text: str):
    """
    text를 받아서 번역하는 코드입니다.
    :param text:
    :return:
    """
    print(f'번역 전 : {text}')
    # 0. tag 변수 체크 및 저장
    tag_pattern = r"<a(.*?)>|</a>|<font(.*?)>|</font>|<b>|</b>|<br>|</br>"
    tag_check = re.findall(tag_pattern, text)
    tag_dict = {}
    # 중복제거
    tag_check = [param[0] for param in list(set(tag_check))]
    # tag 변환
    for i in range(len(tag_check)):
        tag_dict[tag_check[i]] = '#'*i
    for k, v in tag_dict.items():
        text = text.replace(k, v)

    # 0. 변수 체크 및 저장
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
    # tag 복구
    for k, v in tag_dict.items():
        translated = translated.replace(v, k)
        translated = re.sub(v, k, translated, flags=re.IGNORECASE)
    print(f'번역 후 : {translated}')
    time.sleep(0.5)
    return translated

def text_replace(path: str):
    """
    변환
    :param path:
    :return:
    """
    from Game.Dict.text.game_dict import dict_game
    with open(path, 'r', encoding='utf-16le') as f:
        text = f.read()
        for k, v in dict_game.items():
            text = text.replace(k, v)
        #저장
    with open(path, 'w', encoding='utf-16le') as f:
        f.write(text)

if __name__ == '__main__':
    # 0. 번역 객체 생성
    translator = Translator()
    # 1. 파일 오픈 및 텍스트 파싱
    path = './start.txt'
    with open(path, 'r', encoding='utf-16le') as f:
        text_list = text_word_parser(all_text=f.read())
    # 2. 텍스트 번역 후 저장
    translator_run(text_list=text_list)

    # 별도. 게임 번역 후 저장
    # text_replace(path=path)