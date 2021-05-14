import os
import json

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
        if act_type not in act_map:
            act_map[act_type] = act["activityID"]
        if act_type not in merge_count:
            merge_count[act_type] = {}
        if vid not in merge_count[act_type]:
            merge_count[act_type][vid] = {}
        if start not in merge_count[act_type][vid]:
            merge_count[act_type][vid][start] = []
        merge_count[act_type][vid][start].append(score)

    for act_type,v in merge_count.items():
        for vid,info in v.items():
            for start,scores in info.items():
                if act_type not in filter_dict:
                    thresh = 2
                else:
                    thresh = 2
                    # thresh = filter_dict[act_type]
                if len(scores)>thresh:
                    scores.sort()
                    scores = scores[-thresh:]
                for score in scores:
                    new_dict["activities"].append({"activity":act_type,"presenceConf":score,
                    "localization":{vid:{start:1,str(int(start)+pred_frames):0}},"activityID":act_map[act_type]})


    json_str = json.dumps(new_dict,indent=4)
    with open(os.path.join(base_path,output_file_name), 'w') as save_json:
        save_json.write(json_str) 


base_path = "/home/kevinq/exps"
input_file_name = "output.json"
output_file_name = "output_spa.json"

simoutaneous_filter(base_path,input_file_name,output_file_name)

    


