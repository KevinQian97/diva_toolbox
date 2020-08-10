import os
import shutil
from multiprocessing import Pool
in_path = "/mnt/ssda/gkang/speed_tst/proposals"
# check_path = "/mnt/ssda/gkang/speed_tst/proposals"
out_path = "/mnt/ssda/kevinq/datasets/imgs_mask_kf1"
if not os.path.exists(out_path):
    os.makedirs(out_path)




def copy_imgs(vid):
    print("Now process vid:{}".format(vid))
    path = os.path.join(in_path,vid)
    tracklets = os.listdir(path)
    tracklets.remove("props.txt")
    for tracklet in tracklets:
        new_folder = vid.strip(".avi")+"_"+str(tracklet)
        new_path = os.path.join(out_path,new_folder)
        assert not os.path.exists(new_path)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        imgs = os.listdir(os.path.join(in_path,vid,tracklet))
        for img in imgs:
            shutil.copy(os.path.join(in_path,vid,tracklet,img),os.path.join(out_path,new_folder,img))
    return

if  __name__ == "__main__":

    n_jobs = 20
    vids = os.listdir(in_path)
    # checks = os.listdir(check_path)
    # # ex_checks = os.listdir("/mnt/hddb/kevinq/gkang_mask_muturk1_5_props")
    # new_vids = []
    # for vid in vids:
    #     if vid not in checks:
    #         if vid.strip(".avi")+".json" in ex_checks:
    #             new_vids.append(vid)
    # print(len(new_vids))

    

    # assert len(new_vids)==732
    pool = Pool(n_jobs)
    pool.map(copy_imgs, vids)
    pool.close()
