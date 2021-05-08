import os
import json
import decord
from decord import VideoReader
pred_frames = 64
thresh = 4

base_path = "/mnt/cache/exps/lijun_dp7"
js = json.load(open(os.path.join(base_path,"output.json"),"r"))
new_dict = {"filesProcessed":[],"activities":[]}
new_dict["filesProcessed"] = js["filesProcessed"]
acts = js["activities"]
merge_count = {}
act_map = {}
for act in acts:
    act_type = act["activity"]
    score = act["presenceConf"]
    vid = list(act["localization"].keys())[0]
    tmps = list(act["localization"][vid].keys())
    for tmp in tmps:
        if tmp=="bbox":
            continue
        if act["localization"][vid][tmp]==1:
            start = tmp
        else:
            end = tmp
    if act_type not in act_map:
        act_map[act_type] = act["activityID"]
    if act_type not in merge_count:
        merge_count[act_type] = {}
    if vid not in merge_count[act_type]:
        merge_count[act_type][vid] = {}
    if start not in merge_count[act_type][vid]:
        merge_count[act_type][vid][start] = []
    merge_count[act_type][vid][start].append(score)

for act_type,v in merge_count.items():
    for vid,info in v.items():
        for start,scores in info.items():
            if len(scores)>thresh:
                scores.sort()
                scores = scores[-thresh:]
            for score in scores:
                new_dict["activities"].append({"activity":act_type,"presenceConf":score,
                "localization":{vid:{start:1,str(int(start)+pred_frames):0}},"activityID":act_map[act_type]})

json_str = json.dumps(new_dict,indent=4)
with open(os.path.join(base_path,"output_spa.json"), 'w') as save_json:
    save_json.write(json_str) 


    
    


