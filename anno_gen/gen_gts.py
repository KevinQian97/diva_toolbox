import json
import os

acts = json.load(open("/home/lijun/downloads/kf1_meta/references/kf1_all.json","r"))["activities"]
gts = "/mnt/hddb/kevinq/kf1_v3/train"
if not os.path.exists("gts"):
    os.makedirs(gts)
new_dict = {}
for act in acts:
    vid = list(act["localization"].keys())[0]
    if vid not in list(new_dict.keys()):
        new_dict[vid] = []
    else:
        new_dict[vid].append(act)

vids = list(new_dict.keys())
for vid in vids:
    vid_dict = {}
    acts = new_dict[vid]
    for i in range(len(acts)):
        act = acts[i]
        frames = list(act["localization"][vid].keys())
        assert len(frames) == 2
        start_frame = -1
        end_frame = -1
        for frame in frames:
            if act["localization"][vid][frame] == 0:
                end_frame = int(frame)
            else:
                start_frame = int(frame)
        event_type = act["activity"]
        vid_dict[str(i)] = {}
        vid_dict[i]["start_frame"] = start_frame
        vid_dict[i]["end_frame"] = end_frame
        vid_dict[i]["event_type"] = event_type
        vid_dict[i]["objects"] = 



