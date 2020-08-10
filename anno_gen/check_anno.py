import os
import json
import numpy
# path = "/mnt/hddb/kevinq/labels_kf1_umd/test_anno.json"
# path_t = "/mnt/hddb/kevinq/labels_kf1_umd/train_anno.json"
# js_t = json.load(open(path_t,"r"))
# ds_t = js_t["database"]
# js = json.load(open(path,"r"))
# ds = js["database"]
# vids = list(ds.keys())
# vids_t = list(ds_t.keys())
# print(len(vids_t))
# overlap_list = []
# for vid in vids:
#     if vid in vids_t:
#         overlap_list.append(vid)
# print(len(overlap_list))
# print(len(vids))
# zero_list = []
# for vid in vids:
#     conf = ds[vid]["annotations"]["conf"]
#     if max(conf)==0:
#         zero_list.append(vid)
# print(len(zero_list))


json_kf1train = json.load(open("./data/kf1_train_align.json","r"))
json_kf1test = json.load(open("./data/kf1_test_align.json","r"))
json_umd_may = json.load(open("./data/umd_may_align.json","r"))

vids_kftr = list(json_kf1train.keys())
vids_kfte = list(json_kf1test.keys())
vids_umd = list(json_umd_may.keys())

new_dict = {}

overlap_list = []
for vid in vids_umd:
    if vid not in vids_kfte:
        new_dict[vid] = json_umd_may[vid]
        overlap_list.append(vid)
print(len(overlap_list))
json_str = json.dumps(new_dict,indent=4)
with open("./data/umd_align.json", 'w') as save_json:
    save_json.write(json_str)



# vids_t = os.listdir("/mnt/hddb/kevinq/gkang_mask_may_props")
# vids = os.listdir("/mnt/hddb/kevinq/nist_meva_v2/test")
# num = 0
# for vid in vids:
#     if vid in vids_t:
#         num+=1
# print(num)