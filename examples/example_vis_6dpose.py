from ocrtoc_dataset_toolkit import OCRTOC_Dataset
from ocrtoc_dataset_toolkit.utils.logging import set_log_level
import cv2
from matplotlib import pyplot as plt
import open3d as o3d
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_root', help='Dataset root directory')
FLAGS = parser.parse_args()

set_log_level('WARNING')

t = OCRTOC_Dataset(root = FLAGS.dataset_root)

################# 2D #################
for scene_id in tqdm(range(5), '2d vis'):
    for image_id in [0, 2]:
        _2d_pose_image = t.vis_6dpose(
            scene_id = scene_id,
            image_id = image_id,
            dimension = 2,
            show = True
        )

################## 3D #################
for scene_id in tqdm(range(t.load_scene_number()), 'generating 3d image wise vis'):
    for image_id in range(5):
        print('scene:{}, image:{}'.format(scene_id, image_id))
        pcd = t.vis_6dpose(
            scene_id = scene_id,
            image_id = image_id,
            dimension = 3,
            show = True
        )
