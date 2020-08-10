import json
import os


aligns = json.load(open("./data/kf1_v3_test_align.json","r"))
augment_dict = {"Pick_Up_Object":"Theft","Set_Down_Object":"abandon_package"}
augments = list(augment_dict.keys())
jname = "./data/kf1_v3_test_align_aug.json"

for k,v in aligns.items():
    for p, acts in v.items():
        events = list(acts.keys())
        for act in events:
            prop = aligns[k][p][act]
            if act in augments:
                aligns[k][p][augment_dict[act]] = prop*0.8

with open(jname,'w') as j:
    json.dump(aligns,j,indent=2)
j.close()