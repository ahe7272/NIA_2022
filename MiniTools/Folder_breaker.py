import os
import shutil

running_path = input('경로 : ')
for (path, dir, files) in os.walk(running_path):
    for item in files:
        try:
            shutil.move(path + '/' + item, running_path + '/' + item)
        except:
            print(path + '/' + item)
            break