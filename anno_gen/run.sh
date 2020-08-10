#python align.py --prop-path ../prop_gen_gkang_mask2/props/ --gt-path ../gt/kf1_multiple/ --out-path data/kf1_test_align.json
#python align.py --prop-path /mnt/ssda/share/mask_prop_gen_code/kf1_train_proposals/json/ --gt-path ../gt/kf1_multiple/ --out-path data/kf1_train_align.json
#python align.py --prop-path /mnt/ssda/share/mask_prop_gen_code/umd_all_proposals/json --gt-path ../gt/umd_cmu_merge_v4/all --out-path data/umd_all_align.json
#python anno_gen.py --train data/kf1_train_align.json --val data/kf1_test_align.json --out data/kf1_anno.json --all
#python anno_gen.py --train data/umd_all_align.json,data/kf1_train_align.json --val data/kf1_test_align.json --out data/umd_anno.json --all
python anno_gen.py --train data/umd_muturk_align.json --out data/muturk_anno.json --all
#python anno_gen.py --train data/kf1_train_align.json,data/kf1_test_align.json --val="" --out data/kf1_all_anno.json --all
python anno_gen.py --train data/kf1_v3_test_align.json --val="" --out data/test_anno_v3_pchen.json --ratio 0
python gkang2cmu.py --prop_dir /home/ubuntu/gkang/speed_tst/proposals --out_dir /mnt/hddb/kevinq/gkang_kf1_mask_speed_tst
python align.py --prop-path /mnt/hddb/kevinq/gkang_kf1_mask_speed_tst/ --gt-path /mnt/ssda/share/pchen/gt/kf1/val/  --out-path data/kf1_v3_train_align.json
python align.py --prop-path /mnt/hddb/kevinq/gkang_mask_kf1_props/train/ --gt-path /mnt/ssda/share/pchen/gt/kf1/train/ --out-path data/kf1_train_align_pchen.json
python align.py --prop-path /mnt/hddb/kevinq/gkang_mask_muturk1_5_props/ --gt-path /mnt/hddb/kevinq/muturk1_5_gt/ --out-path data/umd_muturk_align.json

python align.py --prop-path /data/yijunq/gkang_kf1_mask_speed_tst/ --gt-path /data/yijunq/kf1/train/ --out-path data/kf1_v3_train_align.json
python anno_gen.py --train data/kf1_v3_train_align.json --val="" --out data/train_anno_v3_kf1train_pchen.json --all

python align.py --prop-path /mnt/hddb/Cache/june2020_mask373/exp/speed_tst_v3/props/ --gt-path /mnt/ssda/share/pchen/gt/umd_cmu_merge_v4/all/ --out-path data/umd373_align.json
python anno_gen.py --train=data/kf1_v3_train_s2_aug_align.json  --val=data/kf1_v3_test_s2_align.json --out data/kf1_v3_all_s2_anno.json --all

