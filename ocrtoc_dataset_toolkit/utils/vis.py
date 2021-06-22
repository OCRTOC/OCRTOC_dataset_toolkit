import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import open3d as o3d

def get_random_color():
    """Generate random color to visualize mask

    Returns:
        np.array(3,): The RGB value of the color
    """
    return np.random.randint(0,255,3).astype(np.uint8)

def generate_scene_pointcloud(depth_path, rgb_path, intrinsics, depth_scale):
    '''Generate point cloud from depth image and color image
    
    Args:
        depth_path(str): depth image path.
        rgb_path(str): rgb image path.
        intrinsics(np.array): camera intrinsics matrix.
        depth_scale(float): the depth factor.

    Returns:
        open3d.geometry.PointCloud: the point cloud
    '''
    colors = np.array(Image.open(rgb_path), dtype=np.float32) / 255.0
    depths = np.array(Image.open(depth_path))
    fx, fy = intrinsics[0,0], intrinsics[1,1]
    cx, cy = intrinsics[0,2], intrinsics[1,2]
    
    xmap, ymap = np.arange(colors.shape[1]), np.arange(colors.shape[0])
    xmap, ymap = np.meshgrid(xmap, ymap)

    points_z = depths / depth_scale
    points_x = (xmap - cx) / fx * points_z
    points_y = (ymap - cy) / fy * points_z

    mask = (points_z > 0)
    points = np.stack([points_x, points_y, points_z], axis=-1)
    points = points[mask]
    colors = colors[mask]

    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points)
    cloud.colors = o3d.utility.Vector3dVector(colors)

    return cloud