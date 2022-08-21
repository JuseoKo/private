from PIL import Image
import os

if True:
    img_list = []

def add(Path, Name):
    #하위 디렉토리 이름을 이름정렬 순으로 리스트화
    filenames = os.listdir(Path)

    for filename in filenames:
        #이미지 오픈 + 컨버트
        img = Image.open(Path + '\\' + filename)
        img_convert = img.convert('RGB')
        #컨버트된 이미지를 리스트로 저장
        img_list.append(img_convert)

    # 이미지 pdf화
    main_img = img_list[0]
    main_img.save(f'./{Name}.pdf', save_all=True, append_images=img_list)


# 메인함수 선언
if __name__ == '__main__':
    path = input('폴더 주소 입력 :')
    name = input('저장 이름 입력 :')
    add(path, name)
    print('완료')
