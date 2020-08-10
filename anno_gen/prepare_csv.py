import csv
import json
import os

path = "/mnt/hdda/share/visulization_lijun_splits/splits/kevin"
f = open("./tmp.txt","w")
vids = os.listdir(path)
for vid in vids:
    props = os.listdir(os.path.join(path,vid))
    for prop in props:
        if prop.strip(".mp4").split("_")[-1] == "gt":
            continue
        else:
            f.write(vid+"/"+prop+"\n")


