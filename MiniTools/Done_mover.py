import json
import os 
import shutil

match_path = '//nia/납품데이터/2-121 연안어장 생태환경 피해 유발 해양생물 데이터/진행중/11th_Done(속 완)/Bbox/Bbox'
done_path = '//nia/납품데이터/2-121 연안어장 생태환경 피해 유발 해양생물 데이터/진행중/11th_Done(속 완)/Bbox/Bbox_Done'

for (path, dir, files) in os.walk(match_path): 
    if path.split('\\')[-1] == 'Originals':
        continue
    for item in files:
        if item[-4:] == '.jpg':
            if os.path.isfile(match_path + '/Originals/' + '_'.join(item.split('_')[2:])):
                print(match_path + '/Originals/' + '_'.join(item.split('_')[2:]))
                shutil.move(match_path + '/Originals/' + '_'.join(item.split('_')[2:]), done_path + '/Originals/' + '_'.join(item.split('_')[2:]))    
                shutil.move(match_path + '/' + item, done_path + '/' + item)    
                shutil.move(match_path + '/' + item[:-4] + '.json', done_path + '/' + item[:-4] + '.json')    

            # else:
            #     print('_'.join(item.split('_')[2:6]))
            #     break
                # if '_'.join(item.split('_')[2:5]) not in no_video:
                #     no_video += ['_'.join(item.split('_')[2:5])]

# print(no_video)