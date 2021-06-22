import open3d as o3d
import numpy as np
from .logging import get_main_logger

logger = get_main_logger()

default_voxel_size = 0.002

def combine(pcds, voxel_size = default_voxel_size):
    """Combine several point cloud and apply voxel downsample.

    Args:
        pcds(list of open3d.geometry.PointCloud): list of point cloud.
        voxel_size(float): voxel size.
    
    Returns:
        open3d.geometry.PointCloud: the combined point cloud.
    """
    logger.debug('full scene pcd: begin preprocess')
    out_pcd = merge_pcds(pcds).voxel_down_sample(voxel_size)
    out_pcd = out_pcd.remove_statistical_outlier(3000, 0.5)[0]
    return out_pcd

def merge_pcds(pcds):
    """Merge several point cloud.

    Args:
        pcds(list of open3d.geometry.PointCloud): list of point cloud.
    
    Returns:
        open3d.geometry.PointCloud: the merged point cloud.
    """
    points = np.zeros(shape = (0, 3), dtype = np.float64)
    colors = np.zeros(shape = (0, 3), dtype = np.float64)
    for pcd in pcds:
        points = np.vstack((points, np.asarray(pcd.points)))
        colors = np.vstack((colors, np.asarray(pcd.colors)))
    out_pcd = o3d.geometry.PointCloud()
    out_pcd.points = o3d.utility.Vector3dVector(points)
    out_pcd.colors = o3d.utility.Vector3dVector(colors)
    return out_pcd