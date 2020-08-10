import json
import os


def get_file_index(filesProcessed):
    new_dict = {}
    for f in filesProcessed:
        new_dict[f]={"framerate": 30.0, "selected": {"0": 1, "9000": 0}}
    return new_dict

ref = json.load(open("/home/lijun/downloads/kf1_meta/references/kf1_all.json","r"))
files = ref["filesProcessed"]
print(len(files))
output = json.load(open("/mnt/ssdb/kevinq/adaptive_temporal_shift_module/exp/iod_kf1_all/output.json","r"))
output["filesProcessed"] = files


jname = "/mnt/ssdb/kevinq/adaptive_temporal_shift_module/exp/iod_kf1_all/output-mod.json"
with open(jname,'w') as j:
    json.dump(output,j,indent=2,ensure_ascii=False)

file_dict = get_file_index(files)
jname = "/mnt/ssdb/kevinq/adaptive_temporal_shift_module/exp/iod_kf1_all/file-index.json"
with open(jname,'w') as j:
    json.dump(file_dict,j,indent=2,ensure_ascii=False)
