import json
import os

img_path = "/mnt/hddb/kevinq/gkang_mask_imgs"
folders = os.listdir(img_path)

json_kf1all = json.load(open("./data/kf1_all_anno.json","r"))
json_kf1test = json.load(open("./data/kf1_test_align.json","r"))
json_umd_all = json.load(open("./data/umd_all_align.json","r"))
json_umd_may = json.load(open("./data/umd_may_train_align.json","r"))

js = json_kf1all["database"]
tracks = list(js.keys())
print(len(tracks))
missing_list = []
for track in tracks:
    if not os.path.exists(os.path.join(img_path,track)):
        missing_list.append(track)
print(len(missing_list))
