import json
import os

input_path = "/home/kevinq/datasets/KF1_DET/referemce/kitware_trd7f-all_1171.json"
js = json.load(open(input_path,"r"))
acts = js["activities"]
calc_dict = {}
for act in acts:
    act_type = act["activity"]
    vid = list(act["localization"].keys())[0]
    tmps = list(act["localization"][vid].keys())
    for tmp in tmps:
        if act["localization"][vid][tmp]==1:
            start = int(tmp)
        else:
            end = int(tmp)
    
    if vid not in calc_dict:
        calc_dict[vid] = {}
    if act_type not in calc_dict[vid]:
        calc_dict[vid][act_type] = end-start
    else:
        calc_dict[vid][act_type] += end-start

json_str = json.dumps(calc_dict,indent=4)
with open("./calc.json", 'w') as save_json:
    save_json.write(json_str) 
