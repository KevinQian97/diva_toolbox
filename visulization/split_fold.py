import os
import json 
import shutil

path = "/home/kevinq/vis/round1_gt_vis"
vids = os.listdir(path)


file_kf1 = json.load(open("/home/kevinq/datasets/KF1_DET/findex/kitware_eo-all_257.json","r"))
file_kf1 = list(file_kf1.keys())
file_dp3 = json.load(open("/home/kevinq/datasets/KF1_DET/findex/kitware_trd3-all_386.json","r"))
file_dp3 = list(file_dp3.keys())

org_dir = "/home/kevinq/vis/round1_gt_vis"
kf1_dir = "/home/kevinq/vis/kf1"
dp3_dir = "/home/kevinq/vis/drop1-3"


for fname in file_kf1:
    fname = fname.strip(".avi")
    if not os.path.exists(os.path.join(org_dir,fname)):
        print(os.path.join(org_dir,fname))
        continue
    src = os.path.join(org_dir,fname)
    dst = os.path.join(kf1_dir,fname)
    shutil.move(src,dst)

for fname in file_dp3:
    fname = fname.strip(".avi")
    if not os.path.exists(os.path.join(org_dir,fname)):
        print(os.path.join(org_dir,fname))
        continue
    src = os.path.join(org_dir,fname)
    dst = os.path.join(dp3_dir,fname)
    shutil.move(src,dst)
