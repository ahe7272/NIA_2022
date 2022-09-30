import os
import shutil

original_list = []
path = input('작업자 폴더경로를 입력해주세요. ')
for (path, dir, files) in os.walk(path):
    for item in files:
        original_list += [item[9:]]
print(len(original_list))
print(len(set(original_list)))
path = input('작업자 폴더경로를 입력해주세요. ')
for (path, dir, files) in os.walk(path):
    for item in files:
        if item[:1] == 'O':
            continue
        if item[-4:] == '.jpg':
            if item in original_list:
                print(item)