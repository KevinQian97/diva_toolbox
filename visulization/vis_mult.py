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


vids = ["c006.mp4","c007.mp4","c008.mp4","c009.mp4"]
path = "/home/kevinq/exps/MMML"
vrs = []
writer = cv2.VideoWriter(os.path.join(path,"comb.mp4"), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24, (2560,1440))
frames_num = 0
for vid in vids:
    vr = VideoReader(os.path.join(path,vid))
    frames_num = max(frames_num,len(vr))
    vrs.append(vr)

for fid in range(frames_num):
    cob_im = np.zeros((2560,1440,3))
    for i in range(len(vids)):
        if fid>len(vrs[i]):
            break
        
