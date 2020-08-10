import os
import json


# path = "/mnt/hddb/kevinq/gkang_mask_muturk1_5_props"
# files = os.listdir(path)
# muturk_s = []
# for f in files:
#     if f.split(".")[-2] not in muturk_s:
#         muturk_s.append(f.split(".")[-2])

# path = "/mnt/hddb/kevinq/gkang_mask_kf1_props/test"
# files = os.listdir(path)
# kf1_tst_s = []
# for f in files:
#     if f.split(".")[-2] not in kf1_tst_s:
#         kf1_tst_s.append(f.split(".")[-2])

# num = 0
# for s in muturk_s:
#     if s not in kf1_tst_s:
#         num+=1
#         print(s)

# print(num)

ds = json.load(open("/mnt/ssda/kevinq/temporal-shift-module/anno_gen_alter/data/kf1_anno.json","r"))["database"]
path = "/mnt/ssda/Cache/apr2020_maskkf1all_1588038578/Chunk1/exp/proposals"
props = list(ds.keys())
for prop in props:
    vid = prop.split("_")[0]+".avi"
    pid = prop.split("_")[1]
    if not os.path.exists(os.path.join(path,vid,pid)):
        raise RuntimeError(os.path.join(path,vid,pid))
