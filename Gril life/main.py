import re
import json
from googletrans import Translator


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
    parser_text = parser_text.replace('</font>', '').replace('</b>', '').replace('<b>', '').replace('<center>',
                                                                                                    '').replace(
        '</center>', '').replace('\t', '')
    # 문장 추출 코드
    text_list = re.findall('\"(.*?)\"\n', parser_text)
    # text_list = re.findall('=\'(.*?)\'\n', parser_text)
    # ================================================
    text_list = [s.replace('\\', '') for s in text_list]
    text_list = list(set(text_list))

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
    print(text)
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


if __name__ == '__main__':
    test = '"-kr- Mmm... <<$tmpName>>. I like it so much when you caress my feet. You should definitely do this more often, <<$altName>>. It makes me feel more confident. Enjoy It, <<$altGgName>>. Thanks to you, I fell in love with this fetish and I like to do it myself."'
    # 번역 객체 생성
    translator = Translator()
    google_translator(text=test)
    # open_game_text(path='./text.txt')
