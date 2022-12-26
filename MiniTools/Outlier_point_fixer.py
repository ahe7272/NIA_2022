import json
import glob
import os 
import pandas as pd

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects

wrong_img = []
wrong_points = []

# Bbox search
# for (path, dir, files) in os.walk("D:/6th_check_sea/Boundingbox"):
# # for (path, dir, files) in os.walk("C:/Users/Administrator/Desktop/좌표 비정상/2차과제/Bbox"):
#     for file in files:
#         if file[-5:] == '.json':
#             objects = getjson(path + '/' + file)
#             for i in range(len(objects['shapes'])):
#                 if (objects['shapes'][i]['points'][0][0] > objects['imageWidth']):
#                     if ((objects['shapes'][i]['points'][0][0]) - objects['imageWidth']) > 3: 
#                         wrong_img += [file]
#                     else:
#                         objects['shapes'][i]['points'][0][0] = objects['imageWidth']
#                 if (objects['shapes'][i]['points'][0][0] < 0):
#                     objects['shapes'][i]['points'][0][0] = 0

#                 if (objects['shapes'][i]['points'][1][0] > objects['imageWidth']):
#                     if ((objects['shapes'][i]['points'][1][0]) - objects['imageWidth']) > 3: 
#                         wrong_img += [file]
#                     else:
#                         objects['shapes'][i]['points'][1][0] = objects['imageWidth']
#                 if (objects['shapes'][i]['points'][1][0] < 0):
#                     objects['shapes'][i]['points'][1][0] = 0

#                 if (objects['shapes'][i]['points'][0][1] > objects['imageHeight']):
#                     if ((objects['shapes'][i]['points'][0][1]) - objects['imageHeight']) > 3: 
#                         wrong_img += [file]
#                     else:
#                         objects['shapes'][i]['points'][0][1] = objects['imageHeight']
#                 if (objects['shapes'][i]['points'][0][1] < 0):
#                     objects['shapes'][i]['points'][0][1] = 0

#                 if (objects['shapes'][i]['points'][1][1] > objects['imageHeight']):
#                     if ((objects['shapes'][i]['points'][1][1] > objects['imageHeight'])) > 3: 
#                         wrong_img += [file]
#                     else:
#                         objects['shapes'][i]['points'][1][1] = objects['imageHeight']
#                 if (objects['shapes'][i]['points'][1][1] < 0):
#                     objects['shapes'][i]['points'][1][1] = 0

#                 with open(path + '/' + file, 'w') as j:
#                     json.dump(objects, j, indent='\t')
#                     j.close()

# print(set(wrong_img))

# Polygon search
# for (path, dir, files) in os.walk("C:/Dataset(침적)/라벨링데이터/Test"):
for (path, dir, files) in os.walk('C:/침적 History/moved'):
    for file in files:
        if file[-5:] == '.json':
            objects = getjson(path + '/' + file)
            for label in objects['shapes']:
                for point in label['points']:
                    if (point[0] > objects['imageWidth']):
                        point[0] = objects['imageWidth']
                        # if (point[0] - objects['imageWidth']) > 3: 
                        #     wrong_img += [file]
                        # else:
                        #     point[0] = objects['imageWidth']

                    if (point[0] < 0):
                        point[0] = 0
                        # if abs(point[0]) > 3: 
                        #     wrong_img += [file]
                        # else:
                        #     point[0] = 0

                    if (point[1] > objects['imageHeight']):
                        # if (point[1] - objects['imageHeight']) > 3: 
                        #     wrong_img += [file]
                        # else:
                        #     point[1] = objects['imageHeight']
                        point[1] = objects['imageHeight']
                    if (point[1] < 0):
                        print(file, point[1])
                        point[1] = 0
                        # if abs(point[1]) > 3: 
                        #     wrong_img += [file]
                        # else:
                        #     point[1] = 0
                with open(path + '/' + file, 'w') as j:
                    json.dump(objects, j, indent='\t')
                    j.close()

print(set(wrong_img))