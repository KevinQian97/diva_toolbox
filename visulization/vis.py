import decord
from decord import VideoReader
decord.bridge.set_bridge('torch')
import matplotlib.pyplot as plt
import os
import cv2
import torch
import torchvision
import random
import numpy as np

def draw_box_cmu(im, bbox,id,colors,target=False):
    if target:
        cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,0,255), thickness=3)
        cv2.putText(im,"Target", (max(0,int(bbox[0]-10)),max(0,int(bbox[1]-10))),color=(0,0,255), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
    else:
        cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,255,0), thickness=2)
    return im

def check_iou(bboxa,bboxb):
    cover = min((bboxa[2]-bboxa[0])*(bboxa[3]-bboxa[1]),(bboxb[2]-bboxb[0])*(bboxb[3]-bboxb[1]))
    inter_l = max(bboxa[0],bboxb[0])
    inter_t = max(bboxa[1],bboxb[1])
    inter_r = min(bboxa[2],bboxb[2])
    inter_b = min(bboxa[3],bboxb[3])
    if inter_r-inter_l<0 or inter_b-inter_t<0:
        return 0
    inter = (inter_r-inter_l)*(inter_b-inter_t)
    if inter==0:
        return 0
    else:
        return inter/cover

def sync_tracklets(target,path):
    scenes = os.listdir(path)
    new_dict = {}
    for scene in scenes:
        new_dict[scene] = {}
        pred = open(os.path.join(path,scene,"gt/gt.txt"),"r")
        lines = pred.readlines()
        for line in lines:
            line = line.strip()
            frame,ID,left,top,width,height = line.split(",")[:6]
            ID = int(ID)
            if not ID==target:
                continue
            new_dict[scene][int(frame)-1] = [int(left),int(top),int(left)+int(width),int(top)+int(height)]
    return new_dict

def check_hit(sync_dict,scene,frame,bbox):
    if frame not in sync_dict[scene]:
        return False
    if check_iou(bbox,sync_dict[scene][frame]) > 0.7:
        return True
    else:
        return False

trans = torchvision.transforms.ToPILImage(mode='RGB')
target = 208
path = "/home/kevinq/datasets/aic_20_trac3_dataset/validation/S02"
out_path = os.path.join("/home/kevinq/exps/MMML",str(target))
if not os.path.exists(out_path):
    os.makedirs(out_path)
scenes = os.listdir(path)

preds = []
vids = []
colors = []

# for j in range(100):
#     color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     colors.append(color)

sync_dict = sync_tracklets(target,path)
print(sync_dict)
print(scenes)
for scene in scenes:
    vr = VideoReader(os.path.join(path,scene,"vdo.avi"))
    writer = cv2.VideoWriter(os.path.join(out_path,scene+"_tracks.mp4"), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (vr[0].shape[1],vr[0].shape[0]))
    pred = open(os.path.join(path,scene,"mtsc/mtsc_deepsort_mask_rcnn.txt"),"r")
    lines = pred.readlines()
    cur_id = 0
    img = vr[cur_id].permute(2,0,1)
    img = trans(img)
    print(img.size)
    img.save("./tmp.jpg")
    img = cv2.imread("./tmp.jpg")
    for line in lines:
        line = line.strip()
        frame,ID,left,top,width,height = line.split(",")[:6]
        bbox = [int(float(left)),int(float(top)),int(float(left))+int(float(width)),int(float(top))+int(float(height))]
        frame = int(frame)-1
        while frame != cur_id and cur_id<len(vr):
            cur_id+=1
            writer.write(img)
            img = vr[cur_id].permute(2,0,1)
            img = trans(img).save("./tmp.jpg")
            img = cv2.imread("./tmp.jpg")
        else:
            target = check_hit(sync_dict,scene,frame,bbox)
            img = draw_box_cmu(img,bbox,ID,colors,target)

            





