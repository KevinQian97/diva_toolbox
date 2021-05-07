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

def draw_box_cmu(im, bbox,target):
    cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,0,255), thickness=3)
    cv2.putText(im,target, (max(0,int(bbox[0]-10)),max(0,int(bbox[1]-10))),color=(0,0,255), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
    return im

info = {
        "person_enters_vehicle": {
            "start": 69,
            "end": 125,
            "file": "videos/person_enters_car/20200524_2347083605993277192000134_1.mp4",
            "bbox": [
                675.28,
                484.4,
                814.94,
                824.26
            ]
        },
        "person_opens_car_door": {
            "start": 16,
            "end": 68,
            "file": "videos/person_enters_car/20200524_2347083605993277192000134_1.mp4",
            "bbox": [
                675.28,
                484.4,
                814.94,
                824.26
            ]
        },
        "person_closes_car_door": {
            "start": 126,
            "end": 166,
            "file": "videos/person_enters_car/20200524_2347083605993277192000134_1.mp4",
            "bbox": [
                675.28,
                484.4,
                814.94,
                824.26
            ]
        }
    }

base_path = "/home/kevinq/datasets/pip_250k_full_stabilized"
vid_name = "videos/person_enters_car/20200524_2347083605993277192000134_1.mp4"
vid_path = os.path.join(base_path,vid_name)
vr = VideoReader(vid_path)
seq = {}
trans = torchvision.transforms.ToPILImage(mode='RGB')
writer = cv2.VideoWriter("./vis.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (vr[0].shape[1],vr[0].shape[0]))
for i in range(len(vr)):
    img = vr[i].permute(2,0,1)
    img = trans(img).save("./tmp.jpg")
    img = cv2.imread("./tmp.jpg")
    for k,v in info.items():
        if i>=v["start"] and i<=v["end"]:
            img = draw_box_cmu(img, v["bbox"],k)
    writer.write(img)

