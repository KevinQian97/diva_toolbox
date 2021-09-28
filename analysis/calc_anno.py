import json
import os

gt_path = "/home/kevinq/datasets/KF1_DET/reference/kitware_trd11f-all_2203.json"

acts = json.load(open(gt_path,"r"))["activities"]
count_dict = {}
for act in acts:
    label = act["activity"]
    if label not in count_dict:
        count_dict[label]=1
    else:
        count_dict[label]+=1

total = 0
for k,v in count_dict.items():
    total+=v
total/= len(list(count_dict.keys()))
count_dict["avg"] = total

json_str = json.dumps(count_dict,indent=4)
with open("./num.json", 'w') as save_json:
    save_json.write(json_str) 

