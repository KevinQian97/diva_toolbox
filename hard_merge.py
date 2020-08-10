import os
import json

thred_c = 0.9
thred_s = 0.7

def get_siou(boxa,boxb):
    boxa = list(map(int, boxa.split(", ")))
    boxb = list(map(int, boxb.split(", ")))
    if max(boxa[0],boxb[0])>=min(boxa[2],boxb[2]) or max(boxa[1],boxb[1])>=min(boxa[3],boxb[3]):
        return -1
    else:
        return ((min(boxa[2],boxb[2])-max(boxa[0],boxb[0]))*(min(boxa[3],boxb[3])-max(boxa[1],boxb[1])))/((max(boxa[2],boxb[2])-min(boxa[0],boxb[0]))*(max(boxa[3],boxb[3])-min(boxa[1],boxb[1])))

def split_vids(js):
    new_dict = {}
    files = js["filesProcessed"]
    for f in files:
        new_dict[f] = []
    acts = js["activities"]
    for act in acts:
        video  = list(act["localization"].keys())[0]
        new_dict[video].append(act)
    return new_dict

def save_dict(new_dict,path):
    files = new_dict.keys()
    if not os.path.exists(path):
        os.makedirs(path)
    for f in files:
        jname = os.path.join(path,f.strip(".avi"+".json"))
        j_dict = {"filesProcessed":[f],"activities":new_dict[f]}
        json_str = json.dumps(j_dict,indent=4)
        with open(jname, 'w') as save_json:
            save_json.write(json_str)    


def sort_start(acts,vid,bboxes):
    new_dict = {}
    for act in acts:
        for k,v in act["localization"][vid].items():
            if v == 1:
                start = k
        act["bbox"] = bboxes[vid][act["proposal_id"]]
        if start not in list(new_dict.keys()):
            new_dict[start] = [act]
        else:
            new_dict[start].append(act)
    return new_dict

def prep_boxes(path):
    bboxes = {}
    vids = os.listdir(path)
    for vid in vids:
        bboxes[vid] = {}
        f = open(os.path.join(path,vid,"props.txt"),"r")
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            prop_id = line.split(",")[0]
            bbox = line.split(": ")[-1]
            bboxes[vid][prop_id] = bbox
    return bboxes

def merge(input):
    num = 0
    new_dict = {}
    new_dict["activities"] = []
    starts = list(input.keys())
    starts = list(map(int, starts))
    for idx in range(len(starts)-1):
        pres = str(starts[idx])
        next = str(starts[idx+1])
        pres_acts = input[pres]
        next_acts = input[next]
        for pact in pres_acts:
            flag = False
            for nact in next_acts:
                if nact["activity"]==pact["activity"]:
                    if min(nact["presenceConf"],pact["presenceConf"])/max(nact["presenceConf"],pact["presenceConf"])>=thred_c:
                        if get_siou(nact['bbox'],pact["bbox"]) >= thred_s:
                            flag = True
                            break
            if flag:
                num+=1
                new_act ={}
                new_act["activity"] = pact["activity"]
                new_act["activityID"] = pact["activityID"]
                new_act["presenceConf"] = (pact["presenceConf"]+nact["presenceConf"])/2
                vid = list(pact["localization"].keys())[0]
                if "filesProcessed" not in list(new_dict.keys()):
                    new_dict["filesProcessed"] = [vid]
                start = pres
                end = str(int(next)+(int(next)-int(pres)))
                new_act["localization"] = {vid:{start:"1",end:"0"}}
                new_dict["activities"].append(new_act)
            else:
                new_dict["activities"].append(pact)
    print("Merged {} proposals".format(num))
    return new_dict


if __name__ == "__main__":
    output_dict = {"filesProcessed":[],"activities":[]}
    outname = "/mnt/ssdb/kevinq/adaptive_temporal_shift_module/exp/ttsa_mask_reverse_s2/output_merge.json"
    js = json.load(open("/mnt/ssdb/kevinq/adaptive_temporal_shift_module/exp/ttsa_mask_reverse_s2/output.json","r"))
    bboxes = prep_boxes("/mnt/ssda/gkang/speed_tst/proposals")

    split_dict = split_vids(js)
    vids = list(split_dict.keys())
    for vid in vids:
        print(vid)
        output_dict["filesProcessed"].append(vid)
        sort_dict = sort_start(split_dict[vid],vid,bboxes)
        merge_dict = merge(sort_dict)
        for act in merge_dict["activities"]:
            output_dict["activities"].append(act)
    json_str = json.dumps(output_dict,indent=4)
    with open(outname, 'w') as save_json:
        save_json.write(json_str)   




