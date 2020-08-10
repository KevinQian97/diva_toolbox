import os
import json
import shutil

# prop_path = "/mnt/hddb/Cache/apr2020_mask1029_1588038578/Chunk1/exp/proposals"
# gt_path = "/mnt/ssda/share/pchen/gt/umd_cmu_merge_v4/all"

# out_dir = "/mnt/hddb/Cache/apr2020_mask1029_1588038578/Chunk1/exp/proposals_tmp"
# if not os.path.exists(out_dir):
#     os.makedirs(out_dir)

# props = os.listdir(prop_path)
# gts = os.listdir(gt_path)
# num = 0
# for prop in props:
#     if prop.strip(".avi")+".json" in gts:
#         if not os.path.exists(os.path.join(out_dir,prop)):
#             os.makedirs(os.path.join(out_dir,prop))
#         shutil.copy(os.path.join(prop_path,prop,"props.txt"),os.path.join(out_dir,prop,"props.txt"))
#         num+=1
# print("Totally there are {} of umd_cmu_merge annotations".format(num))

# '''
# prepare the new merged data set for training and reference
# '''

# findexs = json.load(open("/mnt/hddb/kevinq/splits_umd/umd_tst.json","r"))
# tst_names = list(findexs.keys())
# gt_path = "/mnt/hddb/kevinq/umd_cmu_kf1_gt/all"
# tar_path = "/mnt/hddb/kevinq/umd_cmu_kf1_gt/test"
# if not os.path.exists(tar_path):
#     os.makedirs(tar_path)
# gts = os.listdir(gt_path)
# for name in tst_names:
#     name = name.strip(".avi")+".json"
#     shutil.copy(os.path.join(gt_path,name),os.path.join(tar_path,name))


# '''
# Resplit according to lijun's split
# '''

# vids = list(json.load(open("./data/kf1_s2_train_158.json","r")).keys())
# new_train_dict = {}
# new_test_dict = {}
# files = ["./data/kf1_v3_train_align.json","./data/kf1_v3_test_align.json"]
# for f in files:
#     js = json.load(open(f,"r"))
#     for vid,props in js.items():
#         if vid+".avi" in vids:
#             new_train_dict[vid] = props
#         else:
#             new_test_dict[vid] = props

# json_str = json.dumps(new_train_dict,indent=4)
# with open("./data/kf1_v3_train_s2_align.json", 'w') as save_json:
#     save_json.write(json_str)
# json_str = json.dumps(new_test_dict,indent=4)
# with open("./data/kf1_v3_test_s2_align.json", 'w') as save_json:
#     save_json.write(json_str)


# vid_list = []

# path = "/mnt/ssda/kevinq/datasets/imgs_mask_kf1"
# or_align = json.load(open("./data/kf1_v3_train_s2_align.json","r"))
# vids = list(or_align.keys())
# props= os.listdir(path)
# for prop in props:
#     vid = prop.split("_")[0]
#     if vid not in vid_list:
#         vid_list.append(vid)

# print(len(vid_list))
# print(len(vids))
# for vid in vids:
#     if vid not in vid_list:
#         print("Still need wait")
#         print(vid)
# img_path = "/mnt/ssda/gkang/speed_tst/proposals"
# js = json.load(open("/mnt/ssda/kevinq/temporal-shift-module/anno_gen_alter/data/kf1_v3_train_s2_align.json","r"))
# for vid, props in js.items():
#     for pid, events in props.items():
#         assert os.path.exists(os.path.join(img_path,vid+".avi",pid))


ref_all = json.load(open("/home/lijun/downloads/kf1_meta/references/kf1_all.json","r"))
fidx = list(json.load(open("./data/kf1_test_s2.json","r")).keys())
new_dict = {}
new_dict["filesProcessed"] = fidx
new_dict["activities"] = []
acts = ref_all["activities"]
for act in acts:
    if list(act["localization"].keys())[0] in fidx:
        new_dict["activities"].append(act)
json_str = json.dumps(new_dict,indent=4)
with open("/mnt/ssdb/kevinq/adaptive_temporal_shift_module/exp/kf1_test_s2.json", 'w') as save_json:
    save_json.write(json_str)



