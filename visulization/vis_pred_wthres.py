import cv2
import json
import os
import random
from avi_r import AVIReader
import multiprocessing
from multiprocessing import Pool
import numpy as np
def draw_box(im, acts,thresh_dict):
    for act in acts:
        bbox = act["bbox"]
        cat = act["act"]
        if "type" in act:
            typ = act["type"]
            if typ=="pred" or typ=="lijun":
                score = act["score"]
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,255,0), thickness=3)
                if score >= thresh_dict[cat]["0.02"]:
                    cv2.putText(im,str(round(score,5)), (int(bbox[0]),max(0,int(bbox[1])-5)),color=(0,0,255), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
                elif score >= thresh_dict[cat]["0.04"]:
                    cv2.putText(im,str(round(score,5)), (int(bbox[0]),max(0,int(bbox[1])-5)),color=(0,255,255), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
                elif score >= thresh_dict[cat]["0.1"]:
                    cv2.putText(im,str(round(score,5)), (int(bbox[0]),max(0,int(bbox[1])-5)),color=(255,255,0), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
                else:
                    cv2.putText(im,str(round(score,5)), (int(bbox[0]),max(0,int(bbox[1])-5)),color=(255,0,255), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
            elif typ == "gt":
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,0,255), thickness=3)
            elif typ == "spl":
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(255,0,0), thickness=3)                
        else:
            cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(255,255,255), thickness=3)
        # cv2.putText(im,str(cat), (bbox[0],max(0,bbox[1]-5)),color=(0,255,0), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
    return im

def split_box(objects,vid_name,timeline,act_type):
    for obj in objects:
        boxes = obj["localization"][vid_name]
        for k,v in boxes.items():
            if "boundingBox" in v:
                x0 = v["boundingBox"]["x"]
                y0 = v["boundingBox"]["y"]
                x1 = x0 + v["boundingBox"]["w"]
                y1 = y0 + v["boundingBox"]["h"]
                frame = int(k)
                if frame not in timeline:
                    timeline[frame] = []
                timeline[frame].append({"act":act_type,"bbox":[x0,y0,x1,y1],"type":"spl"})
    return timeline

def merge_box(objects,vid_name,typ):
    x0 = 10000
    y0 = 10000
    x1 = 0
    y1 = 0
    if typ == "lijun":
        obj = objects[0]
        boxes = obj["localization"][vid_name]
        for k,v in boxes.items():
            if "boundingBox" in v:
                x0 = v["boundingBox"]["x"]
                y0 = v["boundingBox"]["y"]
                x1 = x0 + v["boundingBox"]["w"]
                y1 = y0 + v["boundingBox"]["h"]
        return [x0,y0,x1,y1]

    for obj in objects:
        boxes = obj["localization"][vid_name]
        for k,v in boxes.items():
            if "boundingBox" not in v:
                continue
            x0 = min(v["boundingBox"]["x"],x0)
            y0 = min(v["boundingBox"]["y"],y0)
            x1 = max(x1,v["boundingBox"]["x"]+v["boundingBox"]["w"])
            y1 = max(y1,v["boundingBox"]["y"]+v["boundingBox"]["h"])
    return [x0,y0,x1,y1]


def gen_timeline(acts,targets,vid_name,typ="pred",timeline=None):
    if timeline == None:
        timeline = {}
    for act in acts:
        act_type = act["activity"]
        score = act["presenceConf"]
        if act["activity"] not in targets:
            continue
        if vid_name not in act["localization"]:
            continue
        tmps = list(act["localization"][vid_name].keys())
        for tmp in tmps:
            if tmp == "bbox":
                continue
            if act["localization"][vid_name][tmp]==1:
                start=int(tmp)
            else:
                end = int(tmp)
        if "objects" in act:
            bbox = merge_box(act["objects"],vid_name,typ)
            if typ == "gt":
                timeline = split_box(act["objects"],vid_name,timeline,act_type)
        else:
            bbox = act["localization"][vid_name]["bbox"]
        for frame in range(start,end+1):
            if frame not in timeline:
                timeline[frame] = []
            timeline[frame].append({"act":act_type,"bbox":bbox,"type":typ,"score":score})
    print(len(list(timeline.keys())))
    return timeline


def visualize(output_dir,video_path,video_name,acts,targets):
    video_file = os.path.join(video_path,video_name)
    timeline = gen_timeline(acts,targets,video_name)
    cap = AVIReader(video_file)
    sizex = cap.width 
    sizey = cap.height
    writer = cv2.VideoWriter(output_dir+'/' + video_name.strip(".avi")+'_viz.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (sizex,sizey))
    success, im = cap.read()
    cur_frame = 1
    while(success):
        if cur_frame in timeline:
            im = draw_box(im,timeline[cur_frame])
        writer.write(im)
        cur_frame+=1
        success,im = cap.read()
    # print(count)
    cap.release()
    writer.release()
    return

def visualize_single(output_dir,video_path,video_name,target,set_x=852,set_y=480,conc_neg=False):
    video_file = os.path.join(video_path,video_name)
    timeline = gen_timeline(acts_gt,[target],video_name,"gt")
    if not len(list(timeline.keys())):
        return
    cap = AVIReader(video_file)
    sizex = cap.width 
    sizey = cap.height
    if not os.path.exists(os.path.join(output_dir,video_name.strip(".avi"))):
        os.makedirs(os.path.join(output_dir,video_name.strip(".avi")))
    if os.path.exists(os.path.join(output_dir,video_name.strip(".avi"),'{}.mp4'.format(target))):
        return
    writer = cv2.VideoWriter(os.path.join(output_dir,video_name.strip(".avi"),'{}.mp4'.format(target)), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (set_x,set_y))
    success, im = cap.read()
    cur_frame = 1
    while success:
        if cur_frame in timeline:
            im = draw_box(im,timeline[cur_frame])
            im = cv2.resize(im,(set_x,set_y))
        if conc_neg:
            im = cv2.resize(im,(set_x,set_y))
        writer.write(im)
        cur_frame+=1
        success,im = cap.read()
    cap.release()
    writer.release()
    return

def visualize_duo(output_dir,video_path,video_name,target,set_x=852,set_y=480,conc_neg=False):
    video_file = os.path.join(video_path,video_name)
    thresh_dict = json.load(open("./thresh.json","r"))
    timeline = gen_timeline(acts_pred,[target],video_name,"lijun")
    timeline = gen_timeline(acts_gt,[target],video_name,"gt",timeline)
    if not len(list(timeline.keys())):
        return
    cap = AVIReader(video_file)
    sizex = cap.width 
    sizey = cap.height
    if not os.path.exists(os.path.join(output_dir,video_name.strip(".avi"))):
        os.makedirs(os.path.join(output_dir,video_name.strip(".avi")))
    if os.path.exists(os.path.join(output_dir,video_name.strip(".avi"),'{}.mp4'.format(target))):
        return
    writer = cv2.VideoWriter(os.path.join(output_dir,video_name.strip(".avi"),'{}.mp4'.format(target)), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (set_x,set_y))
    success, im = cap.read()
    cur_frame = 1
    while success:
        if cur_frame in timeline:
            im = draw_box(im,timeline[cur_frame],thresh_dict)
            im = cv2.resize(im,(set_x,set_y))
        if conc_neg:
            im = cv2.resize(im,(set_x,set_y))
        writer.write(im)
        cur_frame+=1
        success,im = cap.read()
    # print(count)
    cap.release()
    writer.release()
    return

if __name__ == "__main__":
    gt_path = "/home/kevinq/datasets/KF1_DET/reference/kitware_trd7-all_914.json"
    js = json.load(open(gt_path,"r"))

    pred_path = "/home/kevinq/exps/vis/output_mod.json"
    js_p = json.load(open(pred_path,"r"))

    act_types = []
    f = open("./labels_det.txt","r")
    lines = f.readlines()
    for line in lines:
        act_types.append(line.strip())

    
    global acts_gt
    acts_gt = js["activities"]
    global acts_pred
    acts_pred = js_p["activities"]

    files_gt = js_p["filesProcessed"]

    output_dir = "/home/kevinq/vis/meva_round1_vis/pred"
    video_path = "/mnt/data/MEVA/videos"

    args = []
    for fname in files_gt:
        for act in act_types:
            args.append((output_dir,video_path,fname,act))

    pool = Pool(20)

    pool.starmap(visualize_duo,args)