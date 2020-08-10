import json
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--train")
parser.add_argument("--val")
parser.add_argument("--out")
parser.add_argument("--label", default="label.txt")
parser.add_argument("--label-map", default="label_map.json")
parser.add_argument("--ratio", type=float, default=1.0)
parser.add_argument("--thres", type=float, default=0.0)
parser.add_argument("--all", action="store_true")
args = parser.parse_args()
args.train = args.train.split(",") if args.train else []
args.val = args.val.split(",") if args.val else []

label = [i.strip() for i in open(args.label)]
label_map = json.load(open(args.label_map))
label2idx = {v: k for k, v in enumerate(label)}

output = {}
database = {}
output["labels"] = label
output["database"] = database

for split, files in [("training", args.train), ("validation", args.val)]:
    for f in files:
        d = json.load(open(f))
        pos = []
        neg = []
        for video, anno in d.items():
            for idx, score in anno.items():
                idx = video+"_"+idx
                score_ = {label_map[k]: v for k, v in score.items()}
                score = [0]*len(label)
                for k, v in score_.items():
                    score[label2idx[k]] = v
                if max(score) > args.thres:
                    pos.append((idx, score))
                else:
                    neg.append((idx, score))
        print("positivite:", len(pos))
        print("negative:", len(neg))
        random.seed(123456)
        if not args.all:
            neg = random.sample(neg, int(len(pos) * args.ratio))
            print(len(neg))
        for idx, score in pos+neg:
            if idx in database:
                print(idx)
                continue
            # assert idx not in database
            database[idx] = {"subset": split, "annotations": {"conf": score}}

json_str = json.dumps(output,indent=4)
with open(args.out, 'w') as save_json:
    save_json.write(json_str)

