import decord
from decord import VideoReader
from decord import cpu, gpu
import torchvision
import json
import os
decord.bridge.set_bridge('torch')

annot_path = "/home/kevinq/datasets/pip_250k_full_stabilized/str250k_annot.json"
db = json.load(open(annot_path,"r"))["database"]
trans = torchvision.transforms.ToPILImage(mode='RGB')
base_path = "/home/kevinq/datasets/pip_250k_full_stabilized"
enlarge_rate = 0.13
for k,v in db.items():
    file_path = os.path.join(base_path,k.split("$")[0])
    if not os.path.exists(file_path):
        continue
    vr = VideoReader(file_path)
    height,width,_=vr[0].shape 
    idx = (v["annotations"]["start"]+v["annotations"]["end"])//2
    idx = min(len(vr)-1,idx)
    x0,y0,x1,y1 = v["annotations"]["bbox"]
    enlarge_x = (x1-x0)*enlarge_rate
    enlarge_y = (y1-y0)*enlarge_rate
    x0 = int(max(0,x0-enlarge_x))
    x1 = int(min(width,x1+enlarge_x))
    y0 = int(max(0,y0-enlarge_y))
    y1 = int(min(height,y1+enlarge_y))
    try:
        img = vr[idx][y0:y1,x0:x1].permute(2,0,1)
        img=trans(img).convert('RGB')
    except:
        print(k) 
        print(y0,y1,x0,x1)
        print(v)

    
