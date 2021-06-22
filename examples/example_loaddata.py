from ocrtoc_dataset_toolkit import OCRTOC_Dataset
from ocrtoc_dataset_toolkit.utils.logging import set_log_level
import cv2
from matplotlib import pyplot as plt
import open3d as o3d
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_root', help='Dataset root directory')
FLAGS = parser.parse_args()

set_log_level('WARNING')

t = OCRTOC_Dataset(root = FLAGS.dataset_root)

# load basic data
scene_name_list = t.load_scene_name_list()
print('Scene Name List:{}'.format(scene_name_list))
object_name_list, object_id_dict = t.load_object_list()
print('Object Name List:{}\nObject Id Dict:{}'.format(object_name_list, object_id_dict))

num_scenes = t.load_scene_number()
num_objects = t.load_object_number()
num_images = t.load_total_image_number()

print('Totally {} scenes, {} different objects, {} images'.format(num_scenes, num_objects, num_images))

# load raw data and annotations
image_id = 4
scene_id = 3

image_number = t.load_scene_image_number(scene_id)
print('scene {} has {} images'.format(scene_id, image_number))

rgb = t.load_raw_image(scene_id = scene_id, image_id = image_id, order = 'RGB')
depth = t.load_depth_image(scene_id = scene_id, image_id = image_id)

pcd = t.load_point_cloud(scene_id = scene_id, image_id = image_id)
seg_mask = t.load_seg_mask(scene_id = scene_id, image_id = image_id)

# cv2.imwrite('color.png', cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
# cv2.imwrite('depth.png', cv2.applyColorMap((depth / 4).astype(np.uint8), cv2.COLORMAP_JET))
# cv2.imwrite('seg_mask.png', cv2.applyColorMap(seg_mask * 10, cv2.COLORMAP_JET))
plt.subplot(3,1,1)
plt.imshow(rgb)
plt.title('RGB image')
plt.subplot(3,1,2)
plt.imshow(depth)
plt.title('Depth image')
plt.subplot(3,1,3)
plt.imshow(seg_mask)
plt.title('Segmentation mask')
plt.show()

# single view image
frame = o3d.geometry.TriangleMesh.create_coordinate_frame(0.1)
o3d.visualization.draw_geometries([pcd, frame])

# full view image
full_pcd = t.load_scene_point_cloud(scene_id = scene_id)
o3d.visualization.draw_geometries([full_pcd, frame])