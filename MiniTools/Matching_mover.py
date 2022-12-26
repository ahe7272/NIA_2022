import os 
import shutil

from_path = input('가져올 파일이 있는 폴더 경로를 입력해주세요. ')
to_path = input('저장할 폴더 경로를 입력해주세요. ')
match_path = input('비교할 파일 경로: ')

for (path, dir, files) in os.walk(match_path): 
    for item in files:
        if item[-4:] == '.jpg':
            if os.path.isfile(to_path + '/' +  '_'.join(item.split('_')[2:])):
                continue
            shutil.move(from_path + '/' + '_'.join(item.split('_')[2:]), to_path + '/' +  '_'.join(item.split('_')[2:]))