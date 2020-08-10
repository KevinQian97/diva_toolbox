import os
import json
import shutil
# split_path = "/mnt/hddb/kevinq/nist_meva_v2"
# train_list = os.listdir(os.path.join(split_path,"train"))
# test_list = os.listdir(os.path.join(split_path,"test"))
# props_path = "/mnt/hddb/kevinq/gkang_mask_kf1_props"
# props = os.listdir(props_path)
# test_folder = os.path.join(props_path,"test")
# if not os.path.exists(test_folder):
#     os.makedirs(test_folder)
# train_folder = os.path.join(props_path,"train")
# if not os.path.exists(train_folder):
#     os.makedirs(train_folder)
# missing_list = []
# train_num = 0
# test_num = 0
# for prop in props:
#     if prop in test_list:
#         shutil.copy(os.path.join(props_path,prop),os.path.join(test_folder,prop))
#         test_num+=1
#     elif prop in train_list:
#         shutil.copy(os.path.join(props_path,prop),os.path.join(train_folder,prop))
#         train_num+=1
#     else:
#         missing_list.append(prop)

# print(missing_list)

# kf1_test_path = "/mnt/hddb/kevinq/gkang_mask_kf1_props/train"
# umd_may_path = "/mnt/hddb/kevinq/gkang_mask_may_props"
# umd_nlp = "/mnt/hddb/kevinq/gkang_mask_may_props_nlp"

# jsons_kftest = os.listdir(kf1_test_path)
# print(len(jsons_kftest))
# jsons_umd = os.listdir(umd_may_path)
# for js in jsons_umd:
#     if js not in kf1_test_path:
#         shutil.copy(os.path.join(umd_may_path,js),os.path.join(umd_nlp,js))


# props_path = "/mnt/hddb/kevinq/gkang_mask_kf1_props/train"
# gts_path = "/mnt/hddb/kevinq/nist_meva_v2/train"
# props = os.listdir(props_path)
# gts = os.listdir(gts_path)
# for prop in props:
#     if prop not in gts:
#         os.remove(os.path.join(props_path,prop))
files = os.listdir("/mnt/hddb/kevinq/gkang_mask_muturk1_5_props")
checks = os.listdir("/mnt/hddb/kevinq/gkang_kf1_mask_speed_tst")
for f in files:
    if f in checks:
        os.remove(os.path.join("/mnt/hddb/kevinq/gkang_mask_muturk1_5_props",f))




