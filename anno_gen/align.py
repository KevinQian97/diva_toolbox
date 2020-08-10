import json
import argparse
import pathlib
import multiprocessing

import util

parser = argparse.ArgumentParser()
parser.add_argument("--prop-path")
parser.add_argument("--gt-path")
parser.add_argument("--out-path")
args = parser.parse_args()

prop = {i.stem: json.load(open(i)) for i in pathlib.Path(args.prop_path).iterdir()}
gt   = {i.stem: json.load(open(i)) for i in pathlib.Path(args.gt_path  ).iterdir()}

# prop = {k: v for k, v in prop.items() if len(v) > 0}
# gt   = {k: v for k, v in gt  .items() if len(v) > 0}
video = list(i for i in prop if i in gt)
prop = {i: prop[i] for i in video}
gt   = {i: gt  [i] for i in video}
print("video count:", len(video))
print("proposal count:", sum(len(i) for i in prop.values()))
print("ground truth count:", sum(len(i) for i in gt.values()))


def score_func(g, p):
    if min(p.project.area, g.project.area) == 0:
        print("project", p.project.area, g.project.area)
    if min(p.length, g.length) == 0:
        print("length", p.length, g.length)
    return (p*g).area/min(p.project.area, g.project.area)/min(p.length, g.length)
    # return (p*g).area/min(p.area, g.area)

pool = multiprocessing.Pool()

def one_video(gt, prop,name,idx):
    print("Now aligning {}, number {}".format(name,idx))
    prop = {k: util.trajectory(v["trajectory"], v["event_begin"], v["event_end"]) for k, v in prop.items()}
    gt, gt_ = {}, gt
    for k, v in gt_.items():
        bbox = util.NDArea(3)
        start_frame = v["start_frame"]
        end_frame = v["end_frame"]
        if "trajectory" in v:
            bbox = bbox + util.trajectory(v["trajectory"], start_frame, end_frame)
        if "objects" in v:
            for o in v["objects"].values():
                bbox = bbox + util.trajectory(o, start_frame, end_frame)
        if bbox.area <= 0:
            print("Warning: empty bounding box for ground truth")
        gt[k] = (bbox, v["event_type"])
    gt_id = list(gt)
    prop_id = list(prop)
    pairs = [(gt[g][0], prop[p]) for p in prop_id for g in gt_id]
    score = pool.starmap(score_func, pairs, chunksize=5)
    score = [score[i*len(gt_id): (i+1)*len(gt_id)] for i in range(len(prop_id))]
    target = {p: {} for p in prop_id}
    for i, g in enumerate(gt_id):
        for j, p in enumerate(prop_id):
            s = score[j][i]
            if s <= 0:
                continue
            if gt[g][1] not in target[p]:
                target[p][gt[g][1]] = 0
            target[p][gt[g][1]] = max(target[p][gt[g][1]], s)
    return target
anno = {i: one_video(gt[i], prop[i],i,video.index(i)) for i in video}
json.dump(anno, open(args.out_path, "w"))
pool.close()
