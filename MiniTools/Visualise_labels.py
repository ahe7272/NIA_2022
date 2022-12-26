import json
import os 
import cv2
import numpy as np
import shutil 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects


for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/test'):
    for file in files:
        if file[-4:] == 'json':
            objects = getjson(path + '/' +file)
            img = cv2.imread(path + '/' + file[:-5] + '.jpg')
            for label in objects['shapes']:
                if label['shape_type'] == 'rectangle': 
                    start = (int(label['points'][0][0]), int(label['points'][0][1]))
                    end = (int(label['points'][1][0]), int(label['points'][1][1]))
                    Text_loc = (int(label['points'][0][0]), int(label['points'][0][1] + 50 ))
                    img = cv2.rectangle(img, start, end, (0, 0, 255), 13)
                    img = cv2.putText(img, label['label'] , Text_loc, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 8)
                
                else:
                    points = []
                    for each_xy in label['points']:
                        x = int(each_xy[0])
                        y = int(each_xy[1])
                        points += [[x, y]]
                    points = np.array(points, np.int32)
                    points = points.reshape((-1,1,2))
                    Text_loc = (points[0][0])
                    img = cv2.polylines(img, [points], True, (0, 0, 255), 5)
                    img = cv2.putText(img, label['label'] , Text_loc, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 8)
                    # cv2.imshow('d', img)
                    # cv2.waitKey(0)
            cv2.imwrite(path + '/Visualised_' + file[:-5] + '.jpg', img)



# for (path, dir, files) in os.walk('C:/조식 History/Bbox'):
#     for file in files:
#         if file[-4:] == 'json':
#             objects = getjson(path + '/' +file)
#             if objects['Distance'] == 0.5:
#                 shutil.copy(path + '/'+ file, 'C:/Users/Administrator/Downloads/f/' + file)
#                 shutil.copy(path + '/'+ file[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/f/' +  file[:-5] + '.jpg')



# # 이미지내 객체 비율
# def ratio_of_objects(objects):
#     height = objects['imageHeight']
#     width = objects['imageWidth']
#     imagesize = height * width 
#     label_with_ratio = [] 
#     maxratio = 0
#     Etc_list = [] 
#     for o in range(len(objects['shapes'])):
#         label = objects['shapes'][o]['label']
#         points = np.array(objects['shapes'][o]['points'])
#         if label == 'Etc':
#             Etc_list += [label]
#             continue
#         # bbx
#         if objects['shapes'][o]['shape_type'] == 'rectangle':
#             object_width = abs(points[0, 0] - points[1, 0])
#             object_height = abs(points[0, 1] - points[1, 1])

#         # polygon
#         else:
#             y = points[:, 0]
#             x = points[:, 1]
#             object_height = max(y) - min(y)    
#             object_width = max(x) - min(x)     
#         object_size = object_height * object_width
#         if maxratio < (object_size / imagesize * 100):
#             maxratio = (object_size / imagesize * 100)
#         label_with_ratio.append((label, object_size / imagesize * 100))
#     if len(Etc_list) == len(objects['shapes']):
#         for o in range(len(objects['shapes'])):
#             label = objects['shapes'][o]['label']
#             points = np.array(objects['shapes'][o]['points'])
#             # bbx
#             if objects['shapes'][o]['shape_type'] == 'rectangle':
#                 object_width = abs(points[0, 0] - points[1, 0])
#                 object_height = abs(points[0, 1] - points[1, 1])

#             # polygon
#             else:
#                 y = points[:, 0]
#                 x = points[:, 1]
#                 object_height = max(y) - min(y)    
#                 object_width = max(x) - min(x)
#             object_size = object_height * object_width
#             if maxratio < (object_size / imagesize * 100):
#                 maxratio = (object_size / imagesize * 100)
#             label_with_ratio.append((label, object_size / imagesize * 100)) 
#     return maxratio, label_with_ratio 

# def classify_distance_4_debris(maxratio):
#     if maxratio <= 20:
#         return 'Far'
#     elif (maxratio <= 60) and (maxratio > 20): 
#         return 'Mid'
#     elif maxratio > 60:
#         return 'Near'

# def classify_distance_4_seaanimal(maxratio, maxlabel):
#     if maxlabel == 'Asterias_amurensis':
#         farratio = 0.9
#         nearratio = 8.09
#     elif maxlabel == 'Asterina_pectinifera':
#         farratio = 0.38
#         nearratio = 3.39
#     elif maxlabel == 'Conch':
#         farratio = 0.06
#         nearratio = 0.5
#     elif maxlabel == 'Ecklonia_cava':
#         farratio = 0
#         nearratio = 0
#     elif maxlabel == 'Heliocidaris_crassispina':
#         farratio = 0.2
#         nearratio = 1.78
#     elif maxlabel == 'Hemicentrotus':
#         farratio = 0.6
#         nearratio = 0.7
#     elif maxlabel == 'Sargassum':
#         farratio = 0
#         nearratio = 0
#     elif maxlabel == 'Sea_hare':
#         farratio = 0.84
#         nearratio = 7.53
#     elif maxlabel == 'Turbo_cornutus':
#         farratio = 0.27
#         nearratio = 2.43
#     if maxratio <= farratio:
#         return 'Far'
#     elif (maxratio <= nearratio) and (maxratio > farratio): 
#         return 'Mid'
#     elif maxratio > nearratio:
#         return 'Near'

# cnt = 0
# for root, dirs, files in os.walk('C:/Users/Administrator/Desktop/조식 10월 2주차까지 Json/bbox'):
#     jsonarr = [Json for Json in files if Json.lower().endswith('json')]
#     for Json in jsonarr:
#         name = os.path.splitext(Json)[0]
#         jsonfile = os.path.join(root, name + '.json')
#         try:
#             objects = getjson(jsonfile)
#         except:
#             continue
#         maxratio, label_with_ratio = ratio_of_objects(objects)
#         if len(label_with_ratio) > 1:
#             for label, ratio in label_with_ratio:
#                 if maxratio == ratio:
#                     maxlabel = label
#         else:
#             maxlabel = label_with_ratio[0][0]   

#         distance_flag = classify_distance_4_seaanimal(maxratio, maxlabel)
#         if maxlabel == 'Heliocidaris_crassispina':
#             if distance_flag == 'Near':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Helio_N/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Helio_N/' +  Json[:-5] + '.jpg')
#             elif distance_flag == 'Mid':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Helio_M/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Helio_M/' +  Json[:-5] + '.jpg')
#             elif distance_flag == 'Far':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Helio_F/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Helio_F/' +  Json[:-5] + '.jpg')

#         elif maxlabel == 'Sea_hare':
#             if distance_flag == 'Near':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/SH_N/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/SH_N/' +  Json[:-5] + '.jpg')
#             elif distance_flag == 'Mid':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/SH_M/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/SH_M/' +  Json[:-5] + '.jpg')
#             elif distance_flag == 'Far':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/SH_F/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/SH_F/' +  Json[:-5] + '.jpg')

#         elif maxlabel == 'Hemicentrotus':
#             if distance_flag == 'Near':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Hemi_N/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Hemi_N/' +  Json[:-5] + '.jpg')
#             elif distance_flag == 'Mid':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Hemi_M/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Hemi_M/' +  Json[:-5] + '.jpg')
            
#         elif maxlabel == 'Turbo_cornutus':
#             if distance_flag == 'Near':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Turbo_N/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Turbo_N/' +  Json[:-5] + '.jpg')
#             elif distance_flag == 'Mid':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Turbo_M/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Turbo_M/' +  Json[:-5] + '.jpg')
#             elif distance_flag == 'Far':
#                 shutil.copy(jsonfile, 'C:/Users/Administrator/Downloads/Turbo_F/' + Json)
#                 shutil.copy(jsonfile[:-5] + '.jpg', 'C:/Users/Administrator/Downloads/Turbo_F/' +  Json[:-5] + '.jpg')