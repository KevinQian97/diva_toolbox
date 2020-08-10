# presently we use kf1 train, umd and umd may  for training and kf1 test for test
import json
import os

json_kf1train = json.load(open("./data/kf1_train_align.json","r"))
json_kf1test = json.load(open("./data/kf1_test_align.json","r"))
json_umd_all = json.load(open("./data/umd_all_align.json","r"))
json_umd_may = json.load(open("./data/umd_may_train_align.json","r"))
merged_name = "./data/gkang_mask_align.json"


# vids1 = list(json_umd_may.keys())
# vids2 = list(json_kf1test.keys())
# inter = list(set(vids1).intersection(set(vids2)))
# print(len(inter))




datasets = [json_kf1train,json_umd_may,json_umd_all]
test_vids = list(json_kf1test.keys())
new_dict = {}
overlap_num = 0
for dataset in datasets:
    vids = list(dataset.keys())
    print(len(vids))
    for vid in vids:
        if vid not in list(new_dict.keys()):
            if vid not in list(test_vids):
                new_dict[vid] = dataset[vid]
            else:
                overlap_num+=1
print(overlap_num)
json.dump(new_dict, open(merged_name, "w"))

