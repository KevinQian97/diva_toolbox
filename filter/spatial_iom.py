import os
import json
import numpy as np

def calc_iom(bboxa,bboxb,thresh=0.8):
    min_w = min(bboxa["w"],bboxb["h"])
    min_h = min(bboxa["w"],bboxb["h"])
    i_x1 = max(bboxa["x"],bboxb["x"])
    i_y1 = max(bboxa["y"],bboxb["y"])
    i_x2 = min(bboxa["x"]+bboxa["w"],bboxb["x"]+bboxb["w"])
    i_y2 = min(bboxa["y"]+bboxa["h"],bboxb["y"]+bboxb["h"])
    i_w = i_x2-i_x1
    i_h = i_y2-i_y1
    if i_w <=0 or i_h<=0 or min_w<=0 or min_h<=0:
        return 0
    elif ((i_w*i_h)/(min_w*min_h))>thresh:
        return 1
    else:
        return 0

def merge_score(scores,thresh=3,iom_num=3):
    iom_mat = np.zeros((len(scores),len(scores)))
    for i in range(len(scores)-1):
        for j in range(i+1,len(scores)):
            iom = calc_iom(scores[i]["bbox"],scores[j]["bbox"])
            iom_mat[i][j] = iom
            iom_mat[j][i] = iom

    keeps = []
    sorts = []
    for i in range(len(scores)):
        if iom_mat[i][i]<0:
            continue
        if np.sum(iom_mat[i])<iom_num:
            keeps.append(scores[i])
        else:
            locs = np.argwhere(iom_mat[i]==1)
            score = 0
            for loc in locs:
                loc = loc[0]
                score+=scores[loc]["score"]
                iom_mat[loc][loc]=-1
            score/=len(locs)
            for j in range(iom_num):
                keeps.append({"score":score,"bbox":{}})
    
    if len(keeps)>thresh:
        for keep in keeps:
            sorts.append(keep["score"])
        sorts.sort()
        sorts = sorts[-thresh:]
        keeps = []
        for sort in sorts:
            keeps.append({"score":sort,"bbox":{}})

    return keeps



def simoutaneous_filter(base_path,input_file_name,output_file_name,tresh_file="./thresh.json",pred_frames=64):
    filter_dict = json.load(open(tresh_file,"r"))
    js = json.load(open(os.path.join(base_path,input_file_name),"r"))
    new_dict = {"filesProcessed":[],"activities":[],"processingReport":{"siteSpecific":{},"fileStatuses":{}}}
    new_dict["filesProcessed"] = js["filesProcessed"]
    for f in new_dict["filesProcessed"]:
        new_dict["processingReport"]["fileStatuses"][f] = {'status': 'success', 'message': ''}
    acts = js["activities"]
    merge_count = {}
    act_map = {}
    for act in acts:
        act_type = act["activity"]
        score = act["presenceConf"]
        vid = list(act["localization"].keys())[0]
        tmps = list(act["localization"][vid].keys())
        for tmp in tmps:
            if tmp=="bbox":
                continue
            if act["localization"][vid][tmp]==1:
                start = tmp
            else:
                end = tmp
        bbox = act["objects"][0]["localization"][vid][start]["boundingBox"]
        if act_type not in act_map:
            act_map[act_type] = act["activityID"]
        if act_type not in merge_count:
            merge_count[act_type] = {}
        if vid not in merge_count[act_type]:
            merge_count[act_type][vid] = {}
        if start not in merge_count[act_type][vid]:
            merge_count[act_type][vid][start] = []
        merge_count[act_type][vid][start].append({"score":score,"bbox":bbox})

    for act_type,v in merge_count.items():
        for vid,info in v.items():
            for start,scores in info.items():
                if act_type not in filter_dict:
                    thresh = 2
                else:
                    thresh = 2
                    # thresh = filter_dict[act_type]
                scores = merge_score(scores,thresh)
                for score in scores:
                    new_dict["activities"].append({"activity":act_type,"presenceConf":score["score"],
                    "localization":{vid:{start:1,str(int(start)+pred_frames):0}},"activityID":act_map[act_type]})


    json_str = json.dumps(new_dict,indent=4)
    with open(os.path.join(base_path,output_file_name), 'w') as save_json:
        save_json.write(json_str) 


base_path = "/home/kevinq/exps/tuning"
input_file_name = "output.json"
output_file_name = "output_spa.json"

simoutaneous_filter(base_path,input_file_name,output_file_name)





