import json
import os

annot_path = "/home/lijun/downloads/road-dataset/road/road_trainval_v1.0.json"
js = json.load(open(annot_path,"r"))
db = js["db"]
ana_dict = {}
for k,v in db.items():
    for id, info in v["action_tubes"].items():
        if info["label_id"] not in ana_dict:
            ana_dict[info["label_id"]] = {"min":len(list(info["annos"].keys())),"max":len(list(info["annos"].keys())),"lst":[len(list(info["annos"].keys()))]}
        else:
            dp = len(list(info["annos"].keys()))
            ana_dict[info["label_id"]]["min"] = min(dp,ana_dict[info["label_id"]]["min"])
            ana_dict[info["label_id"]]["max"] = max(dp,ana_dict[info["label_id"]]["max"])
            ana_dict[info["label_id"]]["lst"].append(dp)

for act,v in ana_dict.items():
    v["avg"] = sum(v["lst"])/len(v["lst"])
    v["lst"] = []

json_str = json.dumps(ana_dict,indent=4)
with open("road_challenge.json", 'w') as save_json:
    save_json.write(json_str)
