import json
import os

gt_folder = "/home/kevinq/datasets/KF1_DET/reference"
gt_name = "kitware_trd3f-all_643.json"
trn_name = "kitware_trd3f_s3-train_394"
tst_name = "kitware_trd3f_s3-test_249"
trn_path = "/home/kevinq/datasets/KF1_DET/proposals/MEVA-kitware_trd3f_s3-train_394"
tst_path = "/home/kevinq/datasets/KF1_DET/proposals/MEVA-kitware_trd3f_s3-test_249"
gt = json.load(open(os.path.join(gt_folder,gt_name),"r"))
trn_dict = {'filesProcessed':[],"activities":[]}
tst_dict = {'filesProcessed':[],"activities":[]}
trn_list = os.listdir(trn_path)
tst_list = os.listdir(tst_path)
for f in gt["filesProcessed"]:
    if f.strip(".avi")+".csv" in trn_list:
        trn_dict["filesProcessed"].append(f)
    else:
        tst_dict["filesProcessed"].append(f)

for act in gt["activities"]:
    vid_name = list(act["localization"].keys())[0]
    if vid_name.strip(".avi")+".csv" in trn_list:
        trn_dict["activities"].append(act)
    else:
        tst_dict["activities"].append(act)

json_str = json.dumps(trn_dict,indent=4)
with open(os.path.join(gt_folder,trn_name+".json"), 'w') as save_json:
    save_json.write(json_str)

json_str = json.dumps(tst_dict,indent=4)
with open(os.path.join(gt_folder,tst_name+".json"), 'w') as save_json:
    save_json.write(json_str)


