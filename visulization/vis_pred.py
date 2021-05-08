import cv2
import json
import os
import random
from avi_r import AVIReader
from multiprocessing import Pool
import numpy as np
def draw_box(im, acts):
    for act in acts:
        bbox = act["bbox"]
        cat = act["act"]
        if "type" in act:
            typ = act["type"]
            if typ=="pred":
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,255,0), thickness=3)
            else:
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,0,255), thickness=3)
        else:
            cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,255,0), thickness=3)
        # cv2.putText(im,str(cat), (bbox[0],max(0,bbox[1]-5)),color=(0,255,0), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
    return im

def merge_box(objects,vid_name):
    x0 = 10000
    y0 = 10000
    x1 = 0
    y1 = 0
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
            bbox = merge_box(act["objects"],vid_name)
        else:
            bbox = act["localization"][vid_name]["bbox"]
        act_type = act["activity"]
        for frame in range(start,end+1):
            if frame not in timeline:
                timeline[frame] = []
            timeline[frame].append({"act":act_type,"bbox":bbox,"type":typ})
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

def visualize_duo(output_dir,video_path,video_name,acts_gt,acts_pred,targets):
    video_file = os.path.join(video_path,video_name)
    timeline = gen_timeline(acts_pred,targets,video_name)
    timeline = gen_timeline(acts_gt,targets,video_name,"gt",timeline)
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

if __name__ == "__main__":
    gt_path = "/home/kevinq/datasets/KF1_DET/referemce/kitware_eo_s2-test_99.json"
    acts_gt = json.load(open(gt_path,"r"))["activities"]
    pred_path = "/mnt/cache/exps/1619759302.8884728/output_mod.json"
    acts_pred = json.load(open(pred_path,"r"))["activities"]
    output_dir = "."
    video_path = "/home/lijun/datasets/actev-datasets/MEVA/videos"
    video_name = "2018-03-11.11-50-00.11-55-00.school.G420.avi"
    targets = ["person_exits_scene_through_structure"]
    visualize_duo(output_dir,video_path,video_name,acts_gt,acts_pred,targets)