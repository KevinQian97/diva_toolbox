import json
import os
import numpy as np

input_path = "/home/kevinq/datasets/KF1_DET/referemce/kitware_trd3f_s2-test_214.json"
gt = json.load(open(input_path,"r"))
acts = gt["activities"]
freq_dict = {}
for act in acts:
    vid_name = list(act["localization"].keys())[0]
    act_type = act["activity"]
    tmps = act["localization"][vid_name].keys()
    for tmp in tmps:
        if act["localization"][vid_name][tmp]==1:
            start = tmp
        else:
            end = tmp
    if act_type not in freq_dict:
        freq_dict[act_type] = {}
    if vid_name not in freq_dict[act_type]:
        freq_dict[act_type][vid_name] = []
    freq_dict[act_type][vid_name].append({"start":int(start),"end":int(end)})

max_count_dict = {}
for act_type, info in freq_dict.items():
    if act_type not in max_count_dict:
        max_count_dict[act_type] = 0
    for vid_name, act_list in freq_dict[act_type].items():
        for frame in range(9000):
            overlap = 0
            for act in act_list:
                if frame>=act["start"] and frame<=act["end"]:
                    overlap+=1
            max_count_dict[act_type] = max(max_count_dict[act_type],overlap)

json_str = json.dumps(max_count_dict,indent=4)
with open("./maxcount.json", 'w') as save_json:
    save_json.write(json_str) 


    