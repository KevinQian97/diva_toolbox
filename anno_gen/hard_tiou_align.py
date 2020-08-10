import os
import json
import multiprocessing


prop_path = "/mnt/hddb/Cache/apr2020_mask1029_1588038578/Chunk1/exp/props_tmp"
gt_path = "/mnt/ssda/share/pchen/gt/umd_cmu_merge_v4/all"
out_path = "./data/tmp_align.json"
labelmap = json.load(open("./label_map.json","r"))
iou_thresh = 0
# if not os.path.exists(out_path):
#     os.makedirs(out_path)

def calc_siou(pbox,gbox):
    x0 = max(pbox[0],gbox[0])
    y0 = max(pbox[1],gbox[1])
    x1 = min(pbox[2],gbox[2])
    y1 = min(pbox[3],gbox[3])
    if x0>=x1 or y0>=y1:
        return 0
    sp = (pbox[2]-pbox[0])*(pbox[3]-pbox[1])
    gp = (gbox[2]-pbox[0])*(pbox[3]-pbox[1])
    if min(sp,gp)==0:
        return 0
    return (x1-x0)*(y1-y0)/min(sp,gp)

def score_label_func(p,g):
    inter_start = max(p[0],g[0])
    inter_end = min(p[1],g[1])
    min_len = min(p[1]-p[0],g[1]-g[0])
    if inter_start>=inter_end:
        return {p[2]:{}}

    elif min_len == 0:
        return {p[2]:{}}
    elif (inter_end-inter_start)/min_len < iou_thresh:
        return {p[2]:{}}
    else:
        tiou = (inter_end-inter_start)/min_len
        frames_pboxes = list(p[3].keys())
        frames_gboxes = list(g[3].keys())
        for f in range(inter_start,inter_end+1):
            if str(f) not in frames_pboxes or str(f) not in frames_gboxes:
                print(g)
                print(frames_pboxes)
                print(frames_gboxes)
                print(f)
                raise RuntimeError()
        pboxes = {f:p[3][str(f)] for f in range(inter_start,inter_end+1)}
        gboxes = {f:g[3][str(f)] for f in range(inter_start,inter_end+1)}
        siou_max = 0
        for f,pbox in pboxes.items():
            gbox = gboxes[f]
            siou = calc_siou(pbox,gbox)
            if siou>siou_max:
                siou_max = siou
        if siou_max==0:
            return {p[2]:{}}
        else:
            return {p[2]:{g[2]:siou_max*tiou}}

pool = multiprocessing.Pool()




def single_video(props,gts):
    se_props = {k: [int(v["event_begin"]), int(v["event_end"]),k,v["trajectory"]] for k, v in props.items()}
    se_gts = {}
    for k, v in gts.items():
        if "trajectory" in list(v.keys()) and v["trajectory"]!={}:
            frames = list(v["trajectory"].keys())
            frames = list(map(int,frames))
            frames.sort()
            start = frames[0]
            end = frames[-1]
            se_gts[k] = [int(start), int(end),labelmap[v["event_type"]],v["trajectory"]]
        if "objects" in list(v.keys()) and v["objects"]!={}:
            for m, n in v["objects"].items():
                frames = list(n.keys())
                frames = list(map(int,frames))
                frames.sort()
                start = frames[0]
                end = frames[-1]
                se_gts[m] = [start, end, labelmap[v["event_type"]], n]
    # se_gts = {k: [int(v["start_frame"]), int(v["end_frame"]),k,v["trajectory"]] for k, v in gts.items()}
    prop_ids = list(se_props.keys())
    prop_gts = list(se_gts.keys())
    pairs = [(se_props[p], se_gts[g]) for p in prop_ids for g in prop_gts]
    scores = pool.starmap(score_label_func, pairs, chunksize=5)
    return scores



prop_jsons=os.listdir(prop_path)
gt_jsons = os.listdir(gt_path)
num = len(prop_jsons)
align_dict = {}
for i in range(len(prop_jsons)):
    f = prop_jsons[i]
    print(f+":{}/{}".format(i,num))
    if f not in gt_jsons:
        continue
    props = json.load(open(os.path.join(prop_path,f),"r"))
    gts = json.load(open(os.path.join(gt_path,f),"r"))
    scores = single_video(props,gts)
    new_dict = {}
    for score in scores:
        assert len(list(score.keys()))==1
        pid = list(score.keys())[0]
        if pid not in list(new_dict.keys()):
            new_dict[pid] = {}
        for e, conf in score[pid].items():
            if e in list(new_dict[pid].keys()):
                if new_dict[pid][e] < conf:
                    new_dict[pid][e] = conf
            else:
                new_dict[pid][e] = conf
    align_dict[f.strip(".json")]=new_dict
with open(out_path,'w') as j:
    json.dump(align_dict,j,indent=2)




    
