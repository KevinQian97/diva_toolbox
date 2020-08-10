import os
import json
from multiprocessing import Pool

input_folder = "/mnt/hddb/kevinq/umd_cmu_kf1_gt/all"
# check_folder = "/mnt/hddb/kevinq/gkang_kf1_mask_speed_tst"
output_folder = "/mnt/hddb/kevinq/umd_cmu_kf1_gt/allsmp"


def interpolate(bboxi,bboxj,i,j,k):
    int_box = []
    assert i<=k
    assert k<=j
    prepi = (k-i)/(j-i)
    prepj = (j-k)/(j-i)
    for i in range(len(bboxi)):
        int_box.append(int(prepi*bboxi[i] + prepj*bboxj[i]))
    return int_box



def interpolates(info):
    new_trajs = {}
    trajectory = info["trajectory"]
    trajs = list(trajectory.keys())
    trajs = list(map(int, trajs))
    trajs.sort()
    trajs = list(map(str, trajs))
    prev = str(info["start_frame"])
    # if end  not in trajs and str(info["end_frame"]-1) not in trajs:
    #     print(end)
    #     print(trajs[-1])
    #     raise RuntimeError("stop")
    prev_bbx = trajectory[prev]
    if prev not in trajs:
        print(prev)
        print(trajs)
    new_trajs[prev] = trajectory[prev]
    idx = 1
    num = len(trajs)
    while idx < num:
        traj = trajs[idx]
        bbx = trajectory[traj]
        assert int(traj)>int(prev)
        if int(traj)-int(prev)>1:
            new_trajs[str(int(prev)+1)] = interpolate(prev_bbx,bbx,int(prev),int(traj),int(prev)+1)
            prev_bbx = new_trajs[str(int(prev)+1)]
        else:
            new_trajs[traj] = trajectory[traj]
            prev_bbx = new_trajs[traj]
            idx +=1
        prev = str(int(prev)+1)

    start = trajs[0]
    end = trajs[-1]
    frames = list(new_trajs.keys())
    for i in range(int(start),int(end)+1):
        if str(i) not in frames:
            raise RuntimeError("frame miss")

    return new_trajs, start, end




def insert(js):
    new_dict = {}
    acts = list(js.keys())
    for act in acts:
        new_dict[act] = {}
        info = js[act]
        new_dict[act]["event_type"] = info["event_type"]
        new_dict[act]["objects"] = info["objects"]
        new_dict[act]["trajectory"], new_dict[act]["start_frame"] ,new_dict[act]["end_frame"] = interpolates(info)
    return new_dict


def api(js_name):
    js = json.load(open(os.path.join(input_folder,js_name),"r"))
    new_dict = insert(js)
    jname = os.path.join(output_folder,js_name)
    with open(jname,'w') as j:
        json.dump(new_dict,j,indent=2)
    j.close()


def main():
    files = os.listdir(input_folder)
    # checks = os.listdir(check_folder)
    # names = []
    # for f in files:
    #     if f not in checks:
    #         names.append(f)
    print(len(files))
    n_jobs = 10
    pool = Pool(n_jobs)
    pool.map(api, files)
    pool.close()


main()

    



        
        
