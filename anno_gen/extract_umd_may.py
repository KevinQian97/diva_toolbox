import shutil
import os
import json
path = "/mnt/hddb/kevinq/umd_may_gts"
json_path = "/home/ubuntu/wenhel/apr2020/p1umd1029orig.json"
js = json.load(open(json_path,"r"))
files = list(js.keys())
ir_list = []
for f in files:
    if js[f]["camera.type"]=="IR":
        ir_list.append(f.strip(".avi")+".json")
files = os.listdir("/mnt/hddb/kevinq/gkang_mask_may")
for f in files:
    if f in ir_list:
        os.remove(os.path.join("/mnt/hddb/kevinq/gkang_mask_may",f))
# files = os.listdir(path)
# for f in files:
#     new_f = f.replace("_",".")
#     if new_f not in (ir_list):
#         shutil.copy(os.path.join(path,f),os.path.join(path,new_f))
# tc_files = os.listdir("/mnt/hddb/kevinq/gkang_mask_may")
# files = os.listdir(path)
# for f in files:
#     if f not in tc_files:
#         os.remove(os.path.join(path,f))


