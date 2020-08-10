import json
import os
import shutil
from multiprocessing import Pool
path = "/mnt/hdda/share/visulization_lijun_splits/tst"
vids = os.listdir(path)
out_dir = "/mnt/hdda/share/visulization_lijun_splits/splits"


def copy(arg):
    vid,inpath,outpath = arg
    print(vid)
    shutil.copytree(os.path.join(inpath,vid),os.path.join(outpath,vid))

def prep_args(path,out_dir,groups):
    args = []
    for i in range(group_num):
        if not os.path.exists(os.path.join(out_dir,"split_{}".format(i))):
            os.makedirs(os.path.join(out_dir,"split_{}".format(i)))
        for vid in groups[i]["vids"]:
            args.append([vid,path,os.path.join(out_dir,"split_{}".format(i))])
    return args

    

group_num = 4
total = 0
count = 0
num_dict = {}
for vid in vids:
    num_dict[vid] = len(os.listdir(os.path.join(path,vid)))-1
    total += num_dict[vid]
    count+=1

print("Totally there are {} events".format(total))
print("Totally there are {} videos".format(count))
ave = total/group_num
print("Average events per-person is {}".format(ave))
# print(num_dict)


groups = []
for i in range(group_num):
    groups.append({"total":0,"vids":[]})
group_idx = 0
for k,v in num_dict.items():
    if groups[group_idx]["total"] < ave or group_idx == (group_num-1):
        groups[group_idx]["total"] += v
        groups[group_idx]["vids"].append(k)
    else:
        group_idx+=1
        groups[group_idx]["total"] += v
        groups[group_idx]["vids"].append(k)    

for i in range(group_num):
    print(groups[i]["total"])
    jname = os.path.join(out_dir,"split_{}.json".format(i+1))
    with open(jname,'w') as j:
        json.dump(groups[i],j,indent=2)
    j.close()

args = prep_args(path,out_dir,groups)
n_jobs = 10
pool = Pool(n_jobs)
pool.map(copy, args)
pool.close()












