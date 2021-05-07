import json
import os
import pandas
import csv

def converter(props,labels,map_dict,vid):
    assert len(list(props.keys()))==len(list(labels.keys()))
    new_dict = {"labels":list(map_dict.keys()),"database":{}}
    for k,v in props.items():
        conf = labels[k]
        tag = vid+"_"+str(k)
        act = {"pos":max(conf)>0,"tid":v["tid"],"annotations":{"conf":conf,"start":v["start"],"end":v["end"],"bbox":v["bbox"]}}
        new_dict["database"][tag] = act
    return new_dict

def prep_map(item):
    map_dict = {}
    for i in range(1,len(item)):
        map_dict[item[i]] = i-1
    return map_dict

def load_props(prop_path):
    props = {}
    csvfile = open(prop_path,"r")
    reader = csv.reader(csvfile)
    for item in reader:
        if reader.line_num == 1:
            # print(item)
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

def filt_neg(annot,ratio=1):
    tags = list(annot["database"].keys())
    random.shuffle(tags)
    print("The number of total annotations:{}".format(len(tags)))
    pos_num = 0
    neg_num = 0
    for tag in tags:
        if annot["database"][tag]["pos"]:
            pos_num +=1
        else:
            neg_num +=1
    if neg_num>0:
        print("Pos/Neg samples is {}".format(pos_num/neg_num))
    neg_num = int(pos_num*ratio)
    new_dict = {"labels":annot["labels"],"database":{}}
    for tag in tags:
        if annot["database"][tag]["pos"]:
            new_dict["database"][tag] = annot["database"][tag]
        else:
            if neg_num>0:
                new_dict["database"][tag] = annot["database"][tag]
                neg_num-=1
    return new_dict

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

def gen_label_virat(prop_path,label_path,neg_rate):
    vids = os.listdir(prop_path)
    annots = []
    for vid in vids:
        print("Now processing VID:{}".format(vid.strip(".csv")))
        props = load_props(os.path.join(prop_path,vid))
        labels,map_dict = load_labels(os.path.join(label_path,vid))
        json_str = json.dumps(map_dict,indent=4)
        with open("./MEVA_DET_label_map.json", 'w') as save_json:
            save_json.write(json_str) 
        annot_dict = converter(props,labels,map_dict,vid.strip(".csv"))
        if neg_rate>0:
            annots.append(filt_neg(annot_dict,neg_rate))
        else:
            annots.append(annot_dict)
    merge_dict = merge(annots)
    return merge_dict

prop_path = "/home/kevinq/datasets/KF1_DET/proposals/MEVA-kitware_eo_s2-test_99"
label_path = "/home/kevinq/datasets/KF1_DET/labels/MEVA-kitware_eo_s2-test_99"
merge_dict = gen_label_virat(prop_path,label_path,0)
splits = [112,168,224]
num_112 = 0
num_224 = 0
num_167 = 0
num_169 = 0
enlarge = 1.13
for k,v in merge_dict["database"].items():
    bbox = v["annotations"]["bbox"]
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]
    if w*enlarge <=splits[0] and h*enlarge<=splits[0]:
        num_112+=1
    elif w*enlarge <=splits[1] and h*enlarge<=splits[1]:
        num_167+=1
    elif w*enlarge <=splits[2] and h*enlarge<=splits[2]:
        num_169 +=1
    else:
        num_224 +=1
    
print(num_112,num_167,num_169,num_224)

