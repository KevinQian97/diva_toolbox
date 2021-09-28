import cv2
import json
import os
import random
from avi_r import AVIReader
import multiprocessing
from multiprocessing import Pool
import numpy as np
import cv2

def draw_box(im, acts,color_dict,show_gt,check_gt=False):
    rm_list = []
    if check_gt:
        gt_act_list = []
        for act in acts:
            cat = act["act"]
            typ = act["type"]
            if typ=="gt" or typ=="spl":
                if cat not in gt_act_list:
                    gt_act_list.append(cat)

    for i in range(len(acts)):
        act = acts[i]
        bbox = act["bbox"]
        cat = act["act"]
        if "type" in act:
            typ = act["type"]
            if typ=="pred" or typ=="lijun":
                if check_gt:
                    if cat not in gt_act_list:
                        continue
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=color_dict[str(cat)], thickness=3)
                im[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])] = im[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]*1.2
                for i in range(3):
                    im[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),i] = im[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),i] + color_dict[str(cat)][i]*0.1
                if str(cat) not in rm_list:
                    cv2.putText(im,str(cat), (20,(len(rm_list)+1)*20),color=color_dict[str(cat)], fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
                    rm_list.append(str(cat))
            elif typ == "gt" and show_gt:
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(255,255,255), thickness=3)
            elif typ == "spl" and show_gt:
                cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0,0,0), thickness=3)                
        else:
            cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(255,255,255), thickness=3)
            cv2.putText(im,str(cat), (bbox[0],max(0,bbox[1]-5)),color=(255,255,255), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
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

def visualize_single(output_dir,video_path,video_name,target,color_dict,set_x=852,set_y=480,conc_neg=False):
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
            im = draw_box(im,timeline[cur_frame],color_dict)
            im = cv2.resize(im,(set_x,set_y))
        if conc_neg:
            im = cv2.resize(im,(set_x,set_y))
        writer.write(im)
        cur_frame+=1
        success,im = cap.read()
    cap.release()
    writer.release()
    return

def visualize_duo(output_dir,video_path,video_name,target,color_dict,set_x=1920,set_y=1080,conc_neg=False,vid_version="r13",record_full=True,show_gt = False):
    video_file = os.path.join(video_path,video_name)
    timeline = gen_timeline(acts_pred,[target],video_name,"lijun")
    timeline = gen_timeline(acts_gt,[target],video_name,"gt",timeline)
    if not len(list(timeline.keys())):
        return
    if vid_version == "r0":
        cap = AVIReader(video_file)
        sizex = cap.width 
        sizey = cap.height
    elif vid_version == "r13":
        cap = cv2.VideoCapture(video_file)
        sizex = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        sizey = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    else:
        raise RuntimeError("video format {} is not supported".format(vid_version))
    
    if not os.path.exists(os.path.join(output_dir,video_name.strip(".avi"))):
        os.makedirs(os.path.join(output_dir,video_name.strip(".avi")))
    if os.path.exists(os.path.join(output_dir,video_name.strip(".avi"),'{}.mp4'.format(target))):
        return
    writer = cv2.VideoWriter(os.path.join(output_dir,video_name.strip(".avi"),'{}.mp4'.format(target)), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (set_x,set_y))
    success, im = cap.read()
    im = im*0.9
    cur_frame = 1
    while success:
        if cur_frame in timeline:
            im = draw_box(im,timeline[cur_frame],color_dict,show_gt)
            im = cv2.resize(im,(set_x,set_y))
        if conc_neg:
            im = cv2.resize(im,(set_x,set_y))
        if record_full:
            im = cv2.resize(im,(set_x,set_y))
        im = np.clip(im,0,255)
        writer.write(np.uint8(im))
        cur_frame+=1
        success,im = cap.read()
        if success:
            im = im*0.9
    # print(count)
    cap.release()
    writer.release()
    return

def visualize_multiduo(output_dir,video_path,video_name,targets,color_dict,set_x=1920,set_y=1080,conc_neg=False,vid_version="r13",record_full=True,show_gt=False,check_gt=False):
    video_file = os.path.join(video_path,video_name)
    timeline = gen_timeline(acts_pred,targets,video_name,"lijun")
    timeline = gen_timeline(acts_gt,targets,video_name,"gt",timeline)
    if not len(list(timeline.keys())):
        return
    if vid_version == "r0":
        cap = AVIReader(video_file)
        sizex = cap.width 
        sizey = cap.height
    elif vid_version == "r13":
        cap = cv2.VideoCapture(video_file)
        sizex = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        sizey = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    else:
        raise RuntimeError("video format {} is not supported".format(vid_version))

    if not os.path.exists(os.path.join(output_dir,video_name.strip(".avi"))):
        os.makedirs(os.path.join(output_dir,video_name.strip(".avi")))
    if os.path.exists(os.path.join(output_dir,video_name.strip(".avi"),'all.mp4')):
        return
    writer = cv2.VideoWriter(os.path.join(output_dir,video_name.strip(".avi"),'all.mp4'), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (set_x,set_y))
    success, im = cap.read()
    im = im*0.5
    cur_frame = 1
    while success:
        if cur_frame in timeline:
            im = draw_box(im,timeline[cur_frame],color_dict,show_gt,check_gt)
            im = cv2.resize(im,(set_x,set_y))
        if conc_neg:
            im = cv2.resize(im,(set_x,set_y))
        if record_full:
            im = cv2.resize(im,(set_x,set_y))
        im = np.clip(im,0,255)
        writer.write(np.uint8(im))
        cur_frame+=1
        success,im = cap.read()
        if success:
            im = im*0.5
    # print(count)
    cap.release()
    writer.release()
    return

if __name__ == "__main__":
    gt_path = "/home/kevinq/datasets/KF1_DET/reference/kitware_eo-all_257.json"
    js = json.load(open(gt_path,"r"))

    pred_path = "/home/kevinq/exps/round3-filt/output-filt-vis.json"
    js_p = json.load(open(pred_path,"r"))

    act_types = []
    f = open("./labels_det.txt","r")
    lines = f.readlines()
    for line in lines:
        act_types.append(line.strip())
    color_list = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),
    (127,255,0),(255,127,0),(127,0,255),(255,0,127),(0,255,127),(0,127,255),
    (50,150,250),(50,250,150),(150,250,50),(150,50,250),(250,150,50),(250,50,150),
    (100,100,200),(200,100,100),(100,200,100),(100,200,200),(200,100,200),(200,200,100),
    (50,150,0),(150,50,0),(50,0,150),(150,0,50),(0,150,50),(0,50,150),
    (100,0,0),(0,100,0),(100,100,0),(100,100,0),(100,0,100),(0,100,100),
    (255,255,255)]
    color_dict = {}
    for i in range(len(act_types)):
        act_type = act_types[i]
        color_dict[act_type] = color_list[i]
    
    global acts_gt
    acts_gt = js["activities"]
    global acts_pred
    acts_pred = js_p["activities"]

    files_gt = js["filesProcessed"]

    output_dir = "/home/kevinq/exps/round3-filt"
    video_path = "/mnt/data/MEVA/videos_r13"

    # visualize_duo(output_dir,video_path,"2018-03-11.16-20-00.16-25-00.bus.G331.avi","person_texts_on_phone",color_dict)
    files = ["2018-03-11.11-45-00.11-50-00.school.G299.avi",
        "2018-03-11.11-55-00.12-00-00.school.G423.avi",
        "2018-03-11.11-25-00.11-30-00.school.G420.avi"
    ]
    for f in files:
        visualize_multiduo(output_dir,video_path,f,act_types,color_dict)
            
    # args = []
    # for fname in files_gt:
    #     for act in act_types:
    #         args.append((output_dir,video_path,fname,act))

    # pool = Pool(20)

    # pool.starmap(visualize_single,args)