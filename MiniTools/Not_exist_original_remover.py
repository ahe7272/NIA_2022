import os
import shutil

to_be_removed_path = input('삭제할 파일이 있는 폴더 경로를 입력해주세요. ')
refer_path = input('존재 여부를 비교할 폴더 경로 ')
removed_path = input('삭제된 파일이 저장될 경로 ')
for (path, dir, files) in os.walk(refer_path): 
    for item in files:
        if item[-4:] == '.jpg':
            if os.path.isfile(to_be_removed_path + '/' + '_'.join(item.split('_')[2:])[:-4] + '_original.jpg'):
                shutil.move(refer_path + '/' + item , removed_path + '/' +item) 
                shutil.move(refer_path + '/' + item[:-4] + '.json' , removed_path + '/' +item[:-4] + '.json')  