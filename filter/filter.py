import os
import json
import pickle
path = "./"
cuboids = pickle.load(open(os.path.join(path,'cuboids-1.5.pkl'),'rb'))
# cam_mappings = pickle.load(open(os.path.join(path,'specific-to-general-mapping.pkl'),'rb'))
label_map = json.load(open(os.path.join(path, 'label-map.json'),'rb'))
thresh_s = 0.1
thresh_e = 0.6
def calc_siou(bboxr,bboxp):
    if max(bboxr[0],bboxp[0])>=min(bboxr[2],bboxp[2]) or max(bboxr[1],bboxp[1])>=min(bboxr[3],bboxp[3]):
        return -1
    else:
        return ((min(bboxr[2],bboxp[2])-max(bboxr[0],bboxp[0]))*(min(bboxr[3],bboxp[3])-max(bboxr[1],bboxp[1])))/((max(bboxr[2],bboxp[2])-min(bboxr[0],bboxp[0]))*(max(bboxr[3],bboxp[3])-min(bboxr[1],bboxp[1])))


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

def if_filt(act,label_map,cuboids,bboxes):
    video  = list(act["localization"].keys())[0]
    scene = video.split(".")[-2]
    vids = cuboids.keys() 
    if scene not in vids:
        return False
    else:
        regions = cuboids[scene]
        tar_reg = None
        max_siou = -1
        for region in regions:
            bboxr = region["bbox"]
            bboxp = bboxes[video][act["proposal_id"]]
            bboxp = list(map(int, bboxp.split(", ")))
            siou = calc_siou(bboxr,bboxp)
            if siou > thresh_s:
                
        if max_siou < thresh_s:
            return True
        else:
            # return False
            if max_siou < thresh_e:
                return False
            else:
                if int(label_map[act["activity"]]) in tar_reg["activities"]:
                    return False
                else:
                    return True


if __name__ == "__main__":
    input_jname = "/home/kevinq/exps/ttsa_mask_reverse_s2/output.json"
    output_jname = "/home/kevinq/exps/ttsa_mask_reverse_s2/output_filt.json"
    prop_path = "/home/kevinq/datasets/KF1_MASK/props_mask_kf1"
    new_dict = {}
    js = json.load(open(input_jname,"r"))
    new_dict["filesProcessed"] = js["filesProcessed"]
    new_dict["activities"] = []
    acts = js["activities"]
    or_num = len(acts)
    bboxes = prep_boxes(prop_path)
    filt_num = 0
    for i in range(len(acts)):
        act = acts[i]
        if i%1000==0:
            print("Already tackle {}/{}, already filter {} preds".format(i,len(acts),filt_num))
        if not if_filt(act,label_map,cuboids,bboxes):
            new_dict["activities"].append(act)
        else:
            filt_num+=1
    json_str = json.dumps(new_dict,indent=4)
    with open(output_jname, 'w') as save_json:
        save_json.write(json_str)   




