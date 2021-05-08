import os
import json
import decord
from decord import VideoReader
base_path = "/mnt/cache/exps/1619759302.8884728"
pred_frames = 64
filter_rate = 0.2
video_path = "/home/lijun/datasets/actev-datasets/MEVA/videos"
# video_path = "/home/kevinq/datasets/VIRAT/videos"
sum_frame = 0
event_path = os.path.join(base_path,"event-wise")
findex = list(json.load(open(os.path.join(base_path,"file-index.json"),"r")).keys())
for vid in findex:
    print(vid)
    vr = VideoReader(os.path.join(video_path,vid))
    sum_frame+=len(vr)

events = os.listdir(event_path)

loc = int(sum_frame/pred_frames*filter_rate)

new_dict = {"filesProcessed":[],"activities":[]}
for event in events:
    rank_list = []
    js = json.load(open(os.path.join(event_path,event,"output.json")))
    acts  = js["activities"]
    print("Now tackle Event:{}".format(event))
    print(len(acts))
    for act in acts:
        rank_list.append(act["presenceConf"])
    rank_list.sort()
    if loc >= len(rank_list):
        loc = len(rank_list)-1
    score = rank_list[-loc]
    for act in acts:
        if act["presenceConf"] >= score:
            new_dict["activities"].append(act)

new_dict["filesProcessed"] = findex

json_str = json.dumps(new_dict,indent=4)
with open(os.path.join(base_path,"output_mod.json"), 'w') as save_json:
    save_json.write(json_str) 



    
    


