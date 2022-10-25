import os
import shutil

for (path, dir, files) in os.walk('D:/To_original/5th'):
    for item in files:
        try:
            shutil.move(path + '/'+item, 'D:/To_original/5th/' + item)
        except:
            print(path + '/' + item)
            break