import json
import os
import shutil
from multiprocessing import Pool

aug_path = "/mnt/ssda/kevinq/datasets/imgs_aug"
base_path = "/mnt/ssda/gkang/speed_tst/proposals"
img_path = "/mnt/ssda/kevinq/datasets/imgs_mask_kf1"
or_align = json.load(open("./data/kf1_v3_train_s2_align.json","r"))
aug_dict = {"Vehicle_Turning_Left":"Vehicle_Reversing","Open_Facility_Door":"Close_Facility_Door"}
aug_keys = list(aug_dict.keys())

def prep_props(vid,props,aug_path,base_path,img_path,or_align,aug_dict,aug_keys):
    print("Now process VID:{}".format(vid))
    new_dict[vid] = props
    aug_idx = len(os.listdir(os.path.join(base_path,vid+".avi")))-1
    for pid,confs in props.items():
        for event,score in confs.items():
            if event in aug_keys:
                new_path = vid+"_"+str(aug_idx)
                print(new_path)
                assert not os.path.exists(os.path.join(img_path,new_path))
                if not os.path.exists(os.path.join(aug_path,new_path)):
                    os.makedirs(os.path.join(aug_path,new_path))
                for i in range(32):
                    img_name = "image_"+str(i).zfill(5)+".jpg"
                    aug_name = "image_"+str(31-i).zfill(5)+".jpg"
                    src = os.path.join(img_path,vid+"_"+str(pid),img_name)
                    tar = os.path.join(aug_path,new_path,aug_name)
                    shutil.copy(src,tar)
                new_confs = {}
                for event,score in confs.items():
                    if event in aug_keys:
                        new_confs[aug_dict[event]] = score
                    else:
                        new_confs[event] = score
                new_dict[vid][aug_idx] = new_confs
                aug_idx+=1
                break


def prep_props_api(args):
    vid = args[0]
    props = args[1]
    aug_path = args[2]
    base_path = args[3]
    img_path = args[4]
    or_align = args[5]
    aug_dict = args[6]
    aug_keys = args[7]
    prep_props(vid,props,aug_path,base_path,img_path,or_align,aug_dict,aug_keys)



new_dict = {}
# args_list = []
for vid,props in or_align.items():
#     args_list.append([vid,props,aug_path,base_path,img_path,or_align,aug_dict,aug_keys])
# n_jobs = 10
# pool = Pool(n_jobs)
# pool.map(prep_props_api, args_list)
# pool.close()

    print("Now process VID:{}".format(vid))
    new_dict[vid] = props.copy()
    aug_idx = len(os.listdir(os.path.join(base_path,vid+".avi")))-1
    for pid,confs in props.items():
        for event,score in confs.items():
            if event in aug_keys:
                new_path = vid+"_"+str(aug_idx)
                print(new_path)
                assert not os.path.exists(os.path.join(img_path,new_path))
                if not os.path.exists(os.path.join(aug_path,new_path)):
                    os.makedirs(os.path.join(aug_path,new_path))
                for i in range(32):
                    img_name = "image_"+str(i).zfill(5)+".jpg"
                    aug_name = "image_"+str(31-i).zfill(5)+".jpg"
                    src = os.path.join(img_path,vid+"_"+str(pid),img_name)
                    tar = os.path.join(aug_path,new_path,aug_name)
                    shutil.copy(src,tar)
                new_confs = {}
                for event,score in confs.items():
                    if event in aug_keys:
                        new_confs[aug_dict[event]] = score
                    else:
                        new_confs[event] = score
                new_dict[vid][aug_idx] = new_confs
                aug_idx+=1
                break

json_str = json.dumps(new_dict,indent=4)
with open("./data/kf1_v3_train_s2_aug_align.json", 'w') as save_json:
    save_json.write(json_str)





