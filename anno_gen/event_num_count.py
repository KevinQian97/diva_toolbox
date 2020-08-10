import os
import json



gt_path = "/mnt/ssda/share/pchen/gt/umd_cmu_merge_v4/all"
jname ="./umd_actcount.json"
event_dict = {}

gts = os.listdir(gt_path)
for gt in gts:
    js = json.load(open(os.path.join(gt_path,gt),"r"))
    for k,v in js.items():
        if not v["event_type"] in event_dict:
            event_dict[v["event_type"]] = 1
        else:
            event_dict[v["event_type"]] += 1
with open(jname,'w') as j:
    json.dump(event_dict,j,indent=4)
j.close()
print(event_dict)
