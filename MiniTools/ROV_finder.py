import json
import datetime
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

ncnt = 0
mcnt = 0
fcnt = 0
elist = [
'Polygon_000001.json',
'Polygon_000002.json',
'Polygon_000003.json',
'Polygon_000004.json',
'Polygon_000005.json',
'Polygon_000006.json',
'Polygon_000007.json',
'Polygon_000008.json',
'Polygon_000009.json',
'Polygon_000010.json',
'Polygon_000309.json',
'Polygon_000447.json',
'Polygon_000454.json',
'Polygon_000555.json',
'Polygon_000556.json',
'Polygon_000557.json',
'Polygon_000559.json',
'Polygon_000560.json',
'Polygon_002462.json',
'Polygon_002463.json',
'Polygon_002464.json',
'Polygon_002465.json',
'Polygon_002466.json',
'Polygon_002469.json',
'Polygon_002470.json',
'Polygon_002472.json',
'Polygon_002473.json',
'Polygon_002474.json',
'Polygon_002475.json',
'Polygon_002477.json',
'Polygon_002480.json',
'Polygon_002482.json',
'Polygon_002485.json',
'Polygon_002488.json',
'Polygon_002489.json',
'Polygon_002490.json',
'Polygon_002495.json',
'Polygon_002503.json',
'Polygon_002508.json',
'Polygon_002509.json',
'Polygon_002512.json',
'Polygon_002513.json',
'Polygon_002514.json',
'Polygon_002564.json',
'Polygon_002565.json',
'Polygon_002566.json',
'Polygon_002567.json',
'Polygon_002568.json',
'Polygon_002570.json',
'Polygon_002571.json',
'Polygon_002572.json',
'Polygon_002574.json',
'Polygon_002581.json',
'Polygon_002586.json',
'Polygon_002597.json',
'Polygon_002606.json',
'Polygon_002607.json',
'Polygon_002609.json',
'Polygon_002610.json',
'Polygon_002613.json',
'Polygon_002615.json',
'Polygon_002617.json',
'Polygon_002618.json'
]
Ec = {}
for (path, dir, files) in os.walk('C:/조식 History/Polygon'): 
    for item in files:
        if item[-5:] == '.json':
            if item in elist:
                continue
            objects = getjson(path + '/' + item)
            if objects['Distance'] == 0.5:
                Ec[item] = 0.5
            elif objects['Distance'] == 1.0:
                Ec[item] = 1.0
            else:
                Ec[item] = 1.5
cnt = 0
# print(ncnt, mcnt, fcnt)
for k, v in Ec.items():
    if v == 0.5:
        cnt += 1

print(cnt)