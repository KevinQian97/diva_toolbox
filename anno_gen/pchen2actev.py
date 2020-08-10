import json
import os

def get_file_index(filesProcessed):
    new_dict = {}
    for f in filesProcessed:
        new_dict[f]={"framerate": 30.0, "selected": {"0": 1, "9000": 0}}
    return new_dict

prop_path = "/mnt/hddb/Cache/june2020_mask373/exp/speed_tst_v1/props"
out_path = "/mnt/ssdb/kevinq/adaptive_temporal_shift_module/exp/umd373_maskv1"
base = json.load(open("data/umd373_anno_v1.json","r"))["database"]
with open("labels.txt","r") as f:
    tmps = f.readlines()
labels = {}
for i in range(len(tmps)):
    tmp = tmps[i].strip()
    labels[i] = tmp 

annos = base.keys()
new_dict = {}
for anno in annos:
    vid = anno.split("_")[0]
    pid = anno.split("_")[-1]
    if vid not in new_dict.keys():
        new_dict[vid] = {}
    info = base[anno]["annotations"]["conf"]
    if max(info)==0:
        continue
    new_dict[vid][anno] = base[anno]
vids = new_dict.keys()
output_dict = {}
output_dict["filesProcessed"] = []
output_dict["activities"] = []

tmps = os.listdir(prop_path)
for tmp in tmps:
    output_dict["filesProcessed"].append(tmp.strip(".json")+".avi")


for vid in vids:
    f = json.load(open(os.path.join(prop_path,vid+".json"),"r"))
    annos = new_dict[vid].keys()
    # output_dict["filesProcessed"].append(vid+".avi")
    for anno in annos:
        pid = anno.split("_")[-1]
        probs = new_dict[vid][anno]["annotations"]["conf"]
        for i in range(len(probs)):
            activity = labels[i]
            activityID = i
            presenceConf = probs[i]
            start = f[str(pid)]["event_begin"]
            end  = f[str(pid)]["event_end"]
            act = {}
            act["activity"] = activity
            act["activityID"] = activityID
            act["presenceConf"] = presenceConf
            act["localization"] = {vid+".avi":{str(start):1,str(end):0}}
            act["proposal_id"] = str(pid)
            output_dict["activities"].append(act)
json_str = json.dumps(output_dict,indent=4)
with open(os.path.join(out_path,"output.json"), 'w') as save_json:
    save_json.write(json_str)

file_dict = get_file_index(output_dict["filesProcessed"])
json_str = json.dumps(file_dict,indent=4)
with open(os.path.join(out_path,"file-index.json"), 'w') as save_json:
    save_json.write(json_str)







        




