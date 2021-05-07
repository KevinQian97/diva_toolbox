import json
import os
import shutil
import glob
from cube import ActivityTypeMEVA,CubeActivities,ActivityTypeVIRAT
import pandas as pd
from merger import OverlapCubeMerger
import csv
import argparse

parser = argparse.ArgumentParser(description="VIS JSON GEN")
parser.add_argument('dataset', type=str,default="DET")
parser.add_argument('--test_list', type=str, default="./test_videofolder.json")
parser.add_argument('--prop_path',type = str,default = "/home/kevinq/datasets/KF1_DET/MEVA-kitware_eo_s2-test_99-filtered_det_v5")
parser.add_argument('--output_filename',type = str,default = "output_vis.json")
parser.add_argument("--vid_type",default=".avi",help="the type of input video files")

args = parser.parse_args()

def merge(annots):
    merge_dict = {"labels":annots[-1]["labels"],"database":{},"files":[]} 
    for annot in annots:
        tags = list(annot["database"].keys())
        for tag in tags:
            # if tag in list(merge_dict["database"].keys()):
            #     print(tag)
            #     raise RuntimeError("rudundant clip")
            vid = tag.split("_")[0]+".avi"
            if vid not in merge_dict["files"]:
                merge_dict["files"].append(vid)
            merge_dict["database"][tag] = annot["database"][tag]
    return merge_dict

def converter(props,labels,map_dict,vid):
    assert len(list(props.keys()))==len(list(labels.keys()))
    new_dict = {"labels":list(map_dict.keys()),"database":{}}
    for k,v in props.items():
        conf = labels[k]
        tag = vid+"_"+str(k)
        act = {"pos":max(conf)>0,"tid":v["tid"],"annotations":{"conf":conf,"start":v["start"],"end":v["end"],"bbox":v["bbox"]}}
        new_dict["database"][tag] = act
        for aug_id,rep_id in aug_dict.items():
            if conf[aug_id]>0 and if_aug:
                aug_conf = []
                for i in conf:
                    aug_conf.append(i)
                aug_conf[rep_id] = aug_conf[aug_id]
                aug_conf[aug_id] = 0
                aug_tag = vid+"_"+str(k)+"_aug_"+str(rep_id)
                aug_act = {"pos":max(aug_conf)>0,"tid":v["tid"],"annotations":{"conf":aug_conf,"start":v["end"],"end":v["start"],"bbox":v["bbox"]}}
                new_dict["database"][aug_tag] = aug_act
    return new_dict

def load_props(prop_path):
    props = {}
    csvfile = open(prop_path,"r")
    reader = csv.reader(csvfile)
    for item in reader:
        if reader.line_num == 1:
            print(item)
            continue
        start = int(float(item[4]))
        end = int(float(item[5]))
        tid = int(float(item[1]))
        bbox = []
        for loc in item[6:]:
            bbox.append(int(float(loc)))
        assert len(bbox)==4
        prop = {"tid":tid,"start":start,"end":end,"bbox":bbox}
        props[item[0]] = prop
    return props

def load_labels(label_path):
    labels = {}
    csvfile = open(label_path,"r")
    reader = csv.reader(csvfile)
    for item in reader:
        if reader.line_num == 1:
            print(item)
            map_dict = prep_map(item)
            continue
        label = list(map(float, item[2:]))
        labels[item[0]] = label
    return labels,map_dict

def prepare_testlist_det_all(args):
    jname = args.test_list
    neg_rate = 0
    annots = []
    vids = os.listdir(os.path.join(args.prop_path,"proposal"))
    for vid in vids:
        print("Now processing VID:{}".format(vid.strip(".csv")))
        props = load_props(os.path.join(args.prop_path,"proposal",vid))
        labels,map_dict = load_labels(os.path.join(args.prop_path,"label",vid))
        annot_dict = converter(props,labels,map_dict,vid.strip(".csv"))
        if neg_rate>0:
            annots.append(filt_neg(annot_dict,neg_rate))
        else:
            annots.append(annot_dict)
        merge_dict = merge(annots)
    json_str = json.dumps(merge_dict,indent=4)
    with open(jname, 'w') as save_json:
        save_json.write(json_str) 
    return

def getoutput_det(res_dict_path,event_dict,args):
    prepare_testlist_det_all(args)
    database = json.load(open(args.test_list,"r"))["database"]
    props = os.listdir(os.path.join(args.prop_path,"proposal"))
    merger = OverlapCubeMerger()
    activities = []
    files = []
    for prop in props:
        vid_name = prop.strip(".csv")
        if vid_name+args.vid_type not in files:
            files.append(vid_name+args.vid_type )
    res = os.listdir(res_dict_path)
    for re in res:
        vid_name = re.strip(".json")
        if vid_name+args.vid_type  not in files:
            files.append(vid_name+args.vid_type ) 
        res_dict = json.load(open(os.path.join(res_dict_path,re),"r"))
        if len(list(res_dict.keys()))==0:
            continue
        cube_tensor = torch.zeros(len(res_dict[vid_name]["props"])*len(event_dict),9)
        for i in range(len(res_dict[vid_name]["props"])):
            prop_name = vid_name+"_"+res_dict[vid_name]["props"][i]
            t0 = float(database[prop_name]["annotations"]["start"])
            t1 = float(database[prop_name]["annotations"]["end"])
            tid = int(database[prop_name]["tid"])
            x0,y0,x1,y1 = database[prop_name]["annotations"]["bbox"]
            for j in range(len(event_dict)):
                score = float(res_dict[vid_name][event_dict[j]][i])
                cube_tensor[i*len(event_dict)+j] = torch.tensor([tid,j+1,score,t0,t1,x0,y0,x1,y1])
            # print(cube_tensor[0])
        if args.dataset in ["MEVA","MASK","DET"]:
            cube_acts = CubeActivities(cube_tensor, vid_name+args.vid_type , ActivityTypeMEVA)
        else:
            cube_acts = CubeActivities(cube_tensor, vid_name+args.vid_type , ActivityTypeVIRAT)

        filtered_acts = merger(cube_acts)
        acts = filtered_acts.to_official()

        # acts = cube_acts.to_official()
        for act in acts:
            act["activityID"] = event_dict.index(act["activity"])
            activities.append(act)
    new_dict = {"filesProcessed":files,"activities":activities}
    file_dict = get_file_index(new_dict["filesProcessed"])
    eve_dict = get_activity_index(event_dict)
    return new_dict,file_dict,eve_dict