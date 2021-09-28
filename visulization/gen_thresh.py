import json
import os


gt_path = "/home/kevinq/exps/vis/output_mod.json"
pred_frames = 64

js = json.load(open(gt_path,"r"))
sum_frame = 9000*len(js["filesProcessed"])
acts = js["activities"]
thresh_dict = {}
rank_dict = {}
with open("./labels_det.txt","r") as f:
    lines = f.readlines()
    for line in lines:
        thresh_dict[line.strip()] = {}
        rank_dict[line.strip()] = []



filter_rates = [0.02,0.04,0.1,0.2]

for act in acts:
    score = act["presenceConf"]
    label = act["activity"]
    rank_dict[label].append(score)

for k,v in rank_dict.items():
    v.sort()
    for rate in filter_rates:
        loc = int(sum_frame/pred_frames*rate)
        if loc >= len(v):
            loc = len(v)-1
        thresh = v[-loc]
        thresh_dict[k][rate] = thresh

json_str = json.dumps(thresh_dict,indent=4)
with open("./thresh.json", 'w') as save_json:
    save_json.write(json_str) 