import os
path = "/mnt/ssda/share/pchen/gt/umd_cmu_merge_v4/all"
files = os.listdir(path)
vids = []
for f in files:
    vids.append(f.strip(".json")+".avi")

g = open("/mnt/hddb/Cache/june2020_mask373/list/umd_video_list.txt","w")
for vid in vids:
    g.write(vid+"\n")

g.close()
