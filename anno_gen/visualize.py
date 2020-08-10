import cv2
import json
import os
import random
from avi_r import AVIReader
from multiprocessing import Pool


def prepare_json_cmu(json_file):
    frame_list = []
    bbox_list = []
    cat_list = []
    id_list = []
    # frame_list.append(-1)
    # bbox_list.append([])
    # id_list.append([])
    for i in range (len(list(json_file.keys()))):
        key = list(json_file.keys())[i]
        tracs = json_file[key]['trajectory']
        frames = tracs.keys()
        for frame in frames:
            target_frame =int(frame)
            bbox = tracs[frame]
            cat = json_file[key]['event_type']
            oid = int(i)
            if target_frame in frame_list:
                bbox_list[frame_list.index(target_frame)].append(bbox)
                id_list[frame_list.index(target_frame)].append(oid)
                cat_list[frame_list.index(target_frame)].append(cat)
            else:
                frame_list.append(target_frame)
                bbox_list.append([])
                bbox_list[-1].append(bbox)
                id_list.append([])
                id_list[-1].append(oid)
                cat_list.append([])
                cat_list[-1].append(cat)
    sorted_framelist = []
    for j in range(len(frame_list)):
        sorted_framelist.append(frame_list[j])
    sorted_framelist.sort()
    sorted_bbox_list = []
    sorted_id_list = []
    sorted_cat_list = []
    for frame in sorted_framelist:
        sorted_bbox_list.append(bbox_list[frame_list.index(frame)])
        sorted_id_list.append(id_list[frame_list.index(frame)])
        sorted_cat_list.append(cat_list[frame_list.index(frame)])
    # print(sorted_framelist)
    return sorted_framelist,sorted_bbox_list,sorted_id_list,sorted_cat_list

def frames_to_timecode(framerate,frames):
    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(frames / (3600 * framerate)),
                                                    int(frames / (60 * framerate) % 60),
                                                    int(frames / framerate % 60),
                                                    int(frames % framerate))

def draw_box_cmu(im, bboxes,cats,ids,colors,json_file):
    for i in range(len(bboxes)):
        bbox = bboxes[i]
        # print(bbox)
        # print(cats)
        oid = ids[i]
        cat = cats[i]
        # print(colors[oid])
        cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=colors[oid], thickness=3)
        # print colors[oid]
        cv2.putText(im,str(cat)+':'+str(list(json_file.keys())[oid]), (0,int(im.shape[0]-30)-30*i),color=colors[oid], fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
        cv2.putText(im,str(list(json_file.keys())[oid]), (max(0,int(bbox[0]-10)),max(0,int(bbox[1]-10))),color=colors[oid], fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)
    return im

def get_clipped_image(im,bbox):
    sizex =im.shape[1]
    sizey =im.shape[0]
    y_1 = bbox[1]
    y_2 = bbox[3]
    x_1 = bbox[0]
    x_2 = bbox[2]
    side = max((y_2-y_1),(x_2-x_1))
    y_1 = int(max(0,y_1-side*0.15))
    y_2 = int(min(sizey,y_2+side*0.15))
    x_1 = int(max(0,x_1-side*0.15))
    x_2 = int(min(sizex,x_2+side*0.15))
    new_im = im[y_1:y_2,x_1:x_2]
    new_im = cv2.resize(new_im,(256,256))
    return new_im

def draw_clipped_videos(jname,video_file,v_folder,video_name):
    new_dict = json.load(open(jname,"r"))
    # cap = cv2.VideoCapture(video_file)
    # change to avi version
    cap = AVIReader(video_file)
    videowriter_list =[]
    start_frame_list = []
    end_frame_list = []
    trajectory_list = []
    event_type_list = []
    for key in list(new_dict.keys()):
        info = new_dict[key]
        start_frame = int(info["start_frame"])
        end_frame = int(info["end_frame"])
        start_frame_list.append(start_frame)
        end_frame_list.append(end_frame)
        event_type = info["event_type"]
        event_type_list.append(event_type)
        trajectory = info["trajectory"]
        trajectory_list.append(trajectory)
        start_time = frames_to_timecode(30,start_frame)
        end_time = frames_to_timecode(30,end_frame)
        videowriter_list.append(cv2.VideoWriter(v_folder+'/' +key+'_'+event_type+'_'+ '_from '+start_time+ ' to '+ end_time +'.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (256,256)))
    count = 0
    success,frame = cap.read()
    while success:
        for key in range(len(start_frame_list)):
            if count >= start_frame_list[key] and count <=end_frame_list[key]:
                if str(count) not in list(trajectory_list[key].keys()):
                    print(trajectory_list[key].keys())
                    print(count)
                    print(event_type_list[key])
                    print(video_name)
                    raise RuntimeError("Missing frames")
                bbox = trajectory_list[key][str(count)]
                clipimg = get_clipped_image(frame,bbox)
                videowriter_list[key].write(clipimg)
        count += 1
        success,frame = cap.read()
    cap.release()
    return


def specially_check_single(jname,video_path,video_name,output_dir):
    # annot= "/mnt/ssda/jingwen/tracking_junwei/2018-03-07_16-50-01_16-55-01_school_G328.avi/annotation/2018-03-07_16-50-01_16-55-01_school_G328/actv_id_type.json"
    # video_path = '/mnt/hddb/share/MEVA/videos'
    # video_name = "2018-03-07_16-50-01_16-55-01_school_G328"
    # output_dir =  "/mnt/hddb/share/playground"
    json_file = json.load(open(jname,"r"))
    frame_list,bbox_list,id_list,cat_list = prepare_json_cmu(json_file)
    video_file = os.path.join(video_path,video_name)
    # cap = cv2.VideoCapture(video_file)
    #convert to avi version
    cap = AVIReader(video_file)
    # sizex = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    sizex = cap.width 
    # sizey = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    sizey = cap.height
    writer = cv2.VideoWriter(output_dir+'/' + video_name.strip(".avi")+'_gt.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (sizex,sizey))
    colors = []
    for j in range(len(json_file.keys())+1):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(color)
    # print(colors)
    print(writer.isOpened())
    count = 0
    cur_frame = 0
    success, im = cap.read()
    while(success):
        if count == frame_list[cur_frame]:
            im = draw_box_cmu(im,bbox_list[cur_frame],cat_list[cur_frame],id_list[cur_frame],colors,json_file)
            if cur_frame < len(frame_list)-1:
                cur_frame += 1
            else:
                break
        # cv2.imwrite('/mnt/ssda/share/test.jpg',im)
        # break
        writer.write(im)
        count+=1
        success,im = cap.read()
    # print(count)
    cap.release()
    writer.release()
    return


def draw_annotations(jname,video_path,video_name,output_dir):
    print("Start generate whole video")
    json_file = json.load(open(jname,"r"))
    frame_list,bbox_list,id_list,cat_list = prepare_json_cmu(json_file)
    video_file = os.path.join(video_path,video_name)
    # cap = cv2.VideoCapture(video_file)
    #convert to avi version
    cap = AVIReader(video_file)
    # sizex = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    sizex = cap.width 
    # sizey = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    sizey = cap.height
    writer = cv2.VideoWriter(output_dir+'/' + video_name.strip(".avi")+'_gt.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (sizex,sizey))
    colors = []
    for j in range(len(json_file.keys())+1):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(color)
    # print(colors)
    print(writer.isOpened())
    count = 0
    cur_frame = 0
    success, im = cap.read()
    if len(frame_list) == 0:
        writer.release()
        print("Void Annotation")
        return

    while(success):
        if count == frame_list[cur_frame]:
            im = draw_box_cmu(im,bbox_list[cur_frame],cat_list[cur_frame],id_list[cur_frame],colors,json_file)
            if cur_frame < len(frame_list)-1:
                cur_frame += 1
            else:
                break
        # cv2.imwrite('/mnt/ssda/share/test.jpg',im)
        # break
        writer.write(im)
        count+=1
        success,im = cap.read()
    # print(count)
    # cap.release()
    writer.release()

    print("Start generate single video")
    new_dict = json.load(open(jname,"r"))
    # cap = cv2.VideoCapture(video_file)
    # change to avi version
    cap = AVIReader(video_file)
    videowriter_list =[]
    start_frame_list = []
    end_frame_list = []
    trajectory_list = []
    event_type_list = []
    for key in list(new_dict.keys()):
        info = new_dict[key]
        start_frame = int(info["start_frame"])
        end_frame = int(info["end_frame"])
        start_frame_list.append(start_frame)
        end_frame_list.append(end_frame)
        event_type = info["event_type"]
        event_type_list.append(event_type)
        trajectory = info["trajectory"]
        trajectory_list.append(trajectory)
        start_time = frames_to_timecode(30,start_frame)
        end_time = frames_to_timecode(30,end_frame)
        videowriter_list.append(cv2.VideoWriter(output_dir+'/' +key+'_'+event_type+'_'+ '_from '+start_time+ ' to '+ end_time +'.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (256,256)))
    count = 0
    success,frame = cap.read()
    while success:
        for key in range(len(start_frame_list)):
            if count >= start_frame_list[key] and count <=end_frame_list[key]:
                if str(count) not in list(trajectory_list[key].keys()):
                    print(trajectory_list[key].keys())
                    print(count)
                    print(event_type_list[key])
                    print(video_name)
                    raise RuntimeError("Missing frames")
                bbox = trajectory_list[key][str(count)]
                clipimg = get_clipped_image(frame,bbox)
                videowriter_list[key].write(clipimg)
        count += 1
        success,frame = cap.read()
    # cap.release()
    return

def draw_annotation_api(arg):
    base_path,jname,video_path,video_name = arg
    output_dir = os.path.join(base_path,video_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print("Presently visualizing the video:{}".format(video_name))
    draw_annotations(jname,video_path,video_name,output_dir)
    # print("Start generate whole video")
    # specially_check_single(jname,video_path,video_name,output_dir)
    # print("Start generate single video")
    # draw_clipped_videos(jname,os.path.join(video_path,video_name),output_dir,video_name)
    return 


def prepare_args(base_path,gt_path,video_paths):
    args = []
    gts = os.listdir(gt_path)
    for gt in gts:
        jname = os.path.join(gt_path,gt)
        video_name = gt.strip(".json")+".avi"
        for path in video_paths:
            if os.path.exists(os.path.join(path,video_name)):
                video_path = path
                break
        assert os.path.exists(os.path.join(video_path,video_name))
        args.append([base_path,jname,video_path,video_name])
    return args



if __name__ == "__main__":
    base_path = "/mnt/hdda/share/visulization_lijun_splits/tst"
    gt_path = "/mnt/hddb/kevinq/umd_cmu_kf1_gt/test"
    video_paths = ["/mnt/hddb/share/MEVA/videos","/mnt/hddb/share/MEVA/kf1"]
    args = prepare_args(base_path,gt_path,video_paths)
    print(len(args))
    n_jobs = 10
    pool = Pool(n_jobs)
    pool.map(draw_annotation_api, args)
    pool.close()

