import json
import os
import numpy as np

prop_path = "/mnt/hddb/kevinq/iod_kf1all_props"


props = os.listdir(prop_path)
scenes = {}
for prop in props:
    scene = prop.split(".")[-2]
    if scene not in list(scenes.keys()):
        scenes[scene] = []
print("There are {} scenes in this data set!".format(len(list(scenes.keys()))))
for prop in props:
    js = json.load(open(os.path.join(prop_path,prop),"r"))
    scene = prop.split(".")[-2]
    for k,v in js.items():
        bbox = v["trajectory"][str(v["start_frame"])]
        size = np.sqrt(np.square(bbox[2]-bbox[0])+np.square(bbox[3]-bbox[1]))
        scenes[scene].append(size)
for k,v in scenes.items():
    print(np.mean(v))
    print(k)

