import json
import os 
import pandas as pd
import numpy as np

running_path = input('경로: ')
new_or_old = '2020'
change_log = {}
original = []
new = []
cnt = 3430

if new_or_old == '2020':
    save_path = '//nia/납품데이터/3-027 해양 침적쓰레기 이미지 고도화 데이터/Dataset(침적)/원천데이터/기구축(화질 개선 후)'
    Original_save_path = '//nia/납품데이터/3-027 해양 침적쓰레기 이미지 고도화 데이터/Dataset(침적)/원천데이터/기구축(화질 개선 전)'
    json_save = '//nia/납품데이터/3-027 해양 침적쓰레기 이미지 고도화 데이터/Dataset(침적)/라벨링데이터/기구축'
else:
    save_path = '//nia/납품데이터/3-027 해양 침적쓰레기 이미지 고도화 데이터/Dataset(침적)/원천데이터/신규구축(화질 개선 후)'
    Original_save_path = '//nia/납품데이터/3-027 해양 침적쓰레기 이미지 고도화 데이터/Dataset(침적)/원천데이터/신규구축(화질 개선 전)'
    json_save = '//nia/납품데이터/3-027 해양 침적쓰레기 이미지 고도화 데이터/Dataset(침적)/라벨링데이터/신규구축'


def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

# 이미지내 객체 비율
def ratio_of_objects(objects):
    height = objects['imageHeight']
    width = objects['imageWidth']
    imagesize = height * width 
    label_with_ratio = [] 
    maxratio = 0
    label_list = []
    for o in range(len(objects['shapes'])):
        label = objects['shapes'][o]['label']
        if label not in label_list:
            label_list += [label]
        points = np.array(objects['shapes'][o]['points'])
        # bbx
        if objects['shapes'][o]['shape_type'] == 'rectangle':
            object_width = abs(points[0, 0] - points[1, 0])
            object_height = abs(points[0, 1] - points[1, 1])
        # polygon
        else:
            y = points[:, 0]
            x = points[:, 1]
            object_height = max(y) - min(y)    
            object_width = max(x) - min(x)     

        object_size = object_height * object_width
        if maxratio < (object_size / imagesize * 100):
            maxratio = (object_size / imagesize * 100)
        label_with_ratio.append((label, object_size / imagesize * 100))
    return maxratio, label_with_ratio, label_list,

def classify_distance_4_debris(maxratio):
    if maxratio <= 20:
        return 'Far'
    elif (maxratio <= 60) and (maxratio > 20): 
        return 'Mid'
    elif maxratio > 60:
        return 'Near'


for (path, dir, files) in os.walk(running_path): 
    if path.split('\\')[-1].split(' ')[-1] == 'Originals':
        continue
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            if len(objects['shapes']) == 0:
                print(item)
                continue   
            maxratio, label_with_ratio, label_list = ratio_of_objects(objects)
            if len(label_with_ratio) > 1:
                for label, ratio in label_with_ratio:
                    if maxratio == ratio:
                        maxlabel = label
            else:
                maxlabel = label_with_ratio[0][0]   
            
            if (maxlabel not in ['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope', 'Rubber_etc', 'Rubber_tire', 'Etc']):
                print(item)
                continue
            if maxlabel == 'Fish_net':
                Final_save = save_path + '/01. 어망류/'
                Final_original = Original_save_path + '/01. 어망류/'
                Final_json = json_save + '/01. 어망류/'
            elif maxlabel == 'Fish_trap':
                Final_save = save_path + '/02. 통발류/'
                Final_original = Original_save_path + '/02. 통발류/'
                Final_json = json_save + '/02. 통발류/'

            elif maxlabel == 'Glass':
                Final_save = save_path + '/03. 유리류/'
                Final_original = Original_save_path + '/03. 유리류/'
                Final_json = json_save + '/03. 유리류/'

            elif maxlabel == 'Metal':
                Final_save = save_path + '/04. 금속류/'
                Final_original = Original_save_path + '/04. 금속류/'
                Final_json = json_save + '/04. 금속류/'

            elif maxlabel == 'Plastic':
                Final_save = save_path + '/05. 플라스틱류/'
                Final_original = Original_save_path + '/05. 플라스틱류/'
                Final_json = json_save + '/05. 플라스틱류/'

            elif maxlabel == 'Wood':
                Final_save = save_path + '/06. 나무류/'
                Final_original = Original_save_path + '/06. 나무류/'
                Final_json = json_save + '/06. 나무류/'

            elif maxlabel == 'Rope':
                Final_save = save_path + '/07. 로프류/'
                Final_original = Original_save_path + '/07. 로프류/'
                Final_json = json_save + '/07. 로프류/'

            elif maxlabel == 'Rubber_etc':
                Final_save = save_path + '/08. 기타고무류/'
                Final_original = Original_save_path + '/08. 기타고무류/'
                Final_json = json_save + '/08. 기타고무류/'

            elif maxlabel == 'Rubber_tire':
                Final_save = save_path + '/09. 기타타이어류/'
                Final_original = Original_save_path + '/09. 기타타이어류/'
                Final_json = json_save + '/09. 기타타이어류/'

            name = new_or_old + '-' + '-'.join(label_list) + '-' + str(cnt).zfill(5)
            old_jpg = path + '/' + item[:-5] + '.jpg'
            new_jpg = Final_save + '/' + name + '.jpg'
            old_json = path + '/' + item
            new_json = Final_json + '/' + name + '.json'
            old_original = path + ' Originals/' + '_'.join(item.split('_')[2:])[:-4] + 'jpg'
            new_original = Final_original + '/' + name + '.jpg'
            original += [old_jpg.split('/')[-1]]
            new += [new_jpg.split('/')[-1]]
            os.rename(old_original, new_original)
            os.rename(old_jpg, new_jpg)
            os.rename(old_json, new_json)
            cnt += 1
            objects = getjson(new_json)
            objects['imagePath'] = name + '.jpg'
            with open(new_json, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()

change_log['Old'] = original
change_log['New'] = new

df = pd.DataFrame(change_log)
df.set_index('Old', inplace = True)

df.to_csv(running_path + '/Name_change_log_Ready_bbox.csv')