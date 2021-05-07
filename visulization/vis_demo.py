import cv2
import os
import matplotlib
import decord
from decord import VideoReader
decord.bridge.set_bridge('torch')
import torch
import torchvision
import numpy as np


targets = [208,101,163,98,123,146,193]
base_path = "/home/kevinq/exps/MMML"
calc_path = "/home/kevinq/datasets/aic_20_trac3_dataset/validation/S02"
frames_perscene = 200
trans = torchvision.transforms.ToPILImage(mode='RGB')

def crop(im1,im2,im3,im4):
    crop_im = np.zeros((1080*2,1920*2,3))
    crop_im[:1080,:1920,:] = im1
    crop_im[1080:,:1920,:] = im2
    crop_im[:1080,1920:,:] = im3
    crop_im[1080:,1920:,:] = im4
    cv2.imwrite("tmp.jpg",crop_im)
    im = cv2.imread("tmp.jpg")
    return im

def load_img(vr,cur_id,trans):
    img = vr[cur_id].permute(2,0,1)
    img = trans(img)
    img.save("./tmp.jpg")
    img = cv2.imread("./tmp.jpg")
    return img

def calc_crop(target,calc_path):
    calc_dict = {}
    scenes = os.listdir(calc_path)
    for scene in scenes:
        calc_dict[scene] = {"start":-1,"end":-1}
        f = open(os.path.join(calc_path,scene,"gt/gt.txt"),"r")
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            frame,ID,left,top,width,height = line.split(",")[:6]
            frame = int(frame)
            ID = int(ID)
            if ID != target:
                continue
            else:
                if calc_dict[scene]["start"] == -1:
                    calc_dict[scene]["start"]=frame
                else:
                    calc_dict[scene]["end"]=frame
    return calc_dict



for target in targets:
    vid_path = os.path.join(base_path,str(target))
    vids = os.listdir(vid_path)
    calc_dict = calc_crop(target,calc_path)
    print(calc_dict)
    frames_dict = {}
    writer = cv2.VideoWriter(os.path.join(vid_path,str(target)+".mp4"), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 15, (1920*2,1080*2))
    for vid in vids:
        vr = VideoReader(os.path.join(vid_path,vid))
        frame_count = len(vr)
        scene = vid.split("_")[0]
        print(scene)
        frames_dict[scene] = []
        start = calc_dict[scene]["start"]
        end = calc_dict[scene]["end"]
        if start == -1:
            start = 0
            end = frames_perscene
        elif end-start < frames_perscene:
            sup_frames = frames_perscene-end+start
            if frame_count-1-end > (sup_frames/2) and start > (sup_frames/2):
                start -= sup_frames/2
                end += sup_frames/2
            elif start < sup_frames/2:
                start = 0
                end += sup_frames-start
            elif frame_count-1-end < sup_frames/2:
                end = frame_count-1
                start -= (sup_frames - (frame_count-1-end))
        else:
            end = start+frames_perscene
        for i in range(int(start),int(end)):
            img = load_img(vr,i,trans)
            frames_dict[scene].append(img)
    min_length = 20000
    scenes = []
    for k,v in frames_dict.items():
        scenes.append(k)
        print(len(v))
        if len(v)<min_length:
            min_length = len(v)
    for i in range(min_length):
        crop_img = crop(frames_dict[scenes[0]][i],frames_dict[scenes[1]][i],frames_dict[scenes[2]][i],frames_dict[scenes[3]][i])
        writer.write(crop_img)


            

        




