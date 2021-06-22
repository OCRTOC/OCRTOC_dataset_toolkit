# Author: Minghao Gou.

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import tempfile
import cv2

from .utils.logging import get_main_logger
from .utils.combine import combine, merge_pcds
from .utils.vis import get_random_color, generate_scene_pointcloud

logger = get_main_logger()

class OCRTOC_Dataset():
    """OCRTOC Dataset toolkit class

    Args:
        root(str): root path for the dataset.
    """
    def __init__(self, root):
        self.root = root
        self.scene_name_list = self.load_scene_name_list()
        self.object_name_list, self.object_id_dict = self.load_object_list()
        
        logger.info('obj name list:{}\nobj id dict:{}\nscene name list:{}'.format(
            self.object_name_list,
            self.object_id_dict,
            self.scene_name_list
            )
        )

    def load_object_list(self, save = False):
        """Load object list.
        
        Args:
            save(bool): save the object list or not.
        
        Returns:
            list, dict: object names and name-id mapping.
        """
        if os.path.exists(os.path.join(self.root, 'object_name_list.txt')):
            f = open(os.path.join(self.root, 'object_name_list.txt'))
            object_name_list = f.readlines()
            f.close()
            object_id_dict = dict()
            for i in range(len(object_name_list)):
                object_name_list[i] = object_name_list[i].strip()
                object_id_dict[object_name_list[i]] = i + 1
            return object_name_list, object_id_dict
        else:
            logger.warning('No existed object list, generate object list from scenes')
            object_name_set = set()
            for scene_id in range(len(self.scene_name_list)):
                scene_object_name_list = self.load_scene_object_list(scene_id)
                for object_name in scene_object_name_list:
                    object_name_set.add(object_name)
            object_name_list = list(object_name_set)
            object_id_dict = dict()
            for i in range(len(object_name_list)):
                object_id_dict[object_name_list[i]] = i + 1
            if save:
                logger.warning('Save object list to dataset folder')
                f = open(os.path.join(self.root, 'object_name_list.txt'), 'w')
                for object_name in object_name_list:
                    f.write(object_name+'\n')
                f.close()
            return object_name_list, object_id_dict
    
    def load_scene_name_list(self, save = False):
        """Load scene name list or generate one
        
        Returns:
            list: scene names.
        """
        scene_list_file_path = os.path.join(self.root, 'scene_name_list.txt')
        if not os.path.exists(scene_list_file_path):
            logger.warning("No existed scene list, generate scene list from scenes")
            scene_name_list = os.listdir(os.path.join(self.root, 'scenes'))
            if save:
                logger.warning('Save scene name list to dataset folder')
                f = open(scene_list_file_path, 'w')
                for i in range(len(scene_name_list)):
                    f.write(scene_name_list[i]+'\n')
                f.close()
        else:
            f = open(scene_list_file_path)
            scene_name_list = f.readlines()
            f.close()
            for i in range(len(scene_name_list)):
                scene_name_list[i] = scene_name_list[i].strip()

        return scene_name_list

    def load_scene_image_number(self, scene_id):
        """Load images number in a scene
    
        Args:
            scene_id(int): scene index.

        Returns:
            int: images number in a scene.
        """
        return len(os.listdir(os.path.join(
            self.root,
            'scenes',
            self.load_scene_name(scene_id),
            'rgb_undistort'
        )))
    
    def load_scene_number(self):
        """Load total scenes number
        
        Returns:
            int: total scenes number in the dataset.
        """
        return len(self.scene_name_list)

    def load_object_number(self):
        """Load total objects number
        
        Returns:
            int: total objects number in the dataset.
        """
        return len(self.object_name_list)

    def load_total_image_number(self):
        """Load total images number
        
        Returns:
            int: total images number in the dataset.
        """
        total_number = 0
        for scene_id in range(self.load_scene_number()):
            total_number += self.load_scene_image_number(scene_id)
        return total_number

    def load_scene_name(self, scene_id):
        """Load scene name
        
        Args:
            scene_id(int): scene index.
        
        Returns:
            str: scene name.
        """
        return self.scene_name_list[scene_id]

    def load_camera_param(self, scene_id):
        """Load camera fake intrinsic matrix for open3d,
        
        Args:
            scene_id(int): scene index.
        
        Returns:
            np.ndarray: fake camera intrinsic matrix.
        """
        logger.warning("Camera parameter retrieved from 'load_camera_param' is not accurate, using 'load_real_camera_intrinsic' instead for accurate result")
        camera_intrin_matrix = np.load(
            os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'color_camK.npy'
            )
        )
        param = o3d.camera.PinholeCameraParameters()
        param.extrinsic = np.eye(4,dtype=np.float64)
        param.intrinsic.set_intrinsics(
            1280,
            720,
            camera_intrin_matrix[0][0],
            camera_intrin_matrix[1][1],
            639.5,
            359.5,
        )
        return param
    
    def load_real_camera_intrinsic(self, scene_id):
        """Load camera real intrinsic matrix
        
        Args:
            scene_id(int): scene index.
        
        Returns:
            np.ndarray: camera intrinsic matrix.
        """
        return np.load(
            os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'color_camK.npy'
            )
        )

    def load_raw_image(self, scene_id, image_id, order = 'RGB'):
        """Load color image
        
        Args:
            scene_id(int): scene index.
            image_id(int): image index.
            order(str): RGB or BGR.
        
        Returns:
            np.ndarray: color image.
        """
        raw_bgr = cv2.imread(
            os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'rgb_undistort',
                '%04d.png' % image_id
            )
        )
        if order == 'BGR':
            return raw_bgr
        elif order == 'RGB':
            return cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2RGB)
        else:
            raise ValueError('Unknown order {}, only RGB and BGR are allowed.'.format(order))
    
    def load_depth_image(self, scene_id, image_id):
        """Load depth image
        
        Args:
            scene_id(int): scene index.
            image_id(int): image index.
        
        Returns:
            np.ndarray: depth image.
        """
        depth = cv2.imread(
            os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'depth_undistort',
                '%04d.png' % image_id
            ),
            cv2.IMREAD_UNCHANGED
        )
        return depth

    def load_camera_pose(self, scene_id, image_id):
        """Load camera poses
        
        Args:
            scene_id(int): scene index.
            image_id(int): image index.
        
        Returns:
            np.ndarray: camera pose with world frame.
        """
        return np.load(os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'camera_poses',
                '%04d.npy' % image_id
            )
        )

    def load_scene_object_list(self, scene_id):
        """Load object list in a scene
        
        Args:
            scene_id(int): scene index.
        
        Returns:
            list: object name list.
        """
        f = open(
            os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'object_list.txt'
            )
        )
        scene_object_name_list = f.readlines()
        f.close()
        for i in range(len(scene_object_name_list)):
            scene_object_name_list[i] = scene_object_name_list[i].strip()
        return scene_object_name_list
    
    def load_object_mesh(self, model_name):
        """Load model mesh file
        
        Args:
            model_name(str): model name.
        
        Returns:
            o3d.geometry.TriangleMesh: model mesh.
        """
        o3d_mesh = o3d.io.read_triangle_mesh(
            os.path.join(
                self.root,
                'rgb_pcd',
                '{}.ply'.format(model_name)
            )
        )
        return o3d_mesh
    

    def load_object_pose_dict(self, scene_id):
        """load object pose in each image
        
        Args:
            scene_id(int): scene index.

        Returns:
            dict: object poses.
        """
        object_pose_dict = dict()
        for object_name in self.load_scene_object_list(scene_id):
            pose_file_path = os.path.join(
                    self.root,
                    'scenes',
                    self.load_scene_name(scene_id),
                    'object_poses',
                    object_name+'.npy'
                )
            if os.path.exists(pose_file_path):
                object_pose_dict[object_name] = np.load(pose_file_path)
            else:
                object_pose_dict[object_name] = None
        return object_pose_dict

    def load_seg_mask(self, scene_id, image_id):
        """load segmentation mask
        
        Args:
            scene_id(int): scene index.
            image_id(int): image index.

        Returns:
            np.ndarray: segmentation mask.
        """
        seg_mask_path = os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'seg_masks',
                '%04d.npy' % image_id
            )
        return np.load(seg_mask_path)

    def load_point_cloud(self, scene_id, image_id):
        """Load partial view point cloud
        
        Args:
            scene_id(int): scene index.
            image_id(int): image index.
        
        Returns:
            o3d.geometry.PointCloud: partial view point cloud.
        """
        pcd = generate_scene_pointcloud(
            depth_path = os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'depth_undistort',
                '%04d.png' % image_id
            ),
            rgb_path = os.path.join(
                self.root,
                'scenes',
                self.load_scene_name(scene_id),
                'rgb_undistort',
                '%04d.png' % image_id
            ),
            intrinsics = self.load_real_camera_intrinsic(scene_id),
            depth_scale = 1000.0
        )
        return pcd

    def load_scene_point_cloud(self, scene_id):
        """Load full view scene point cloud
        
        Args:
            scene_id(int): scene index.
        
        Returns:
            o3d.geometry.PointCloud: Reconstructed point cloud.
        """
        pcds = []
        # one in four of the scenes are used to calculate the full scene
        for image_id in range(0, self.load_scene_image_number(scene_id), 4):
            income_pcd = self.load_point_cloud(scene_id = scene_id, image_id = image_id)
            camera_pose = self.load_camera_pose(scene_id = scene_id, image_id = image_id)
            income_pcd.transform(camera_pose)                
            pcds.append(income_pcd)
        full_pcd = combine(pcds)
        return full_pcd
    
    def vis_6dpose(self, scene_id, image_id = None, dimension = 3, show = True):
        """Visualize 6d pose annotation in a scene or in an image

        Args:
            scene_id(int): the id of the scene.
            image_id(int or None): the id of the image, None for the whole scene.
            dimension(int): 2 for 2d visualization and 3 for 3d visualization.
            show(bool): whether to show the result using open3d.
            
        Returns:
            o3d.geometry.PointCloud or np.array: If dimension==2, returns point cloud; elif 
            dimension == 3, returns BGR image.
        """
        if dimension == 2:
            if image_id is not None:
                bgr = self.load_raw_image(scene_id, image_id, order = 'BGR')
                mask = self.load_seg_mask(scene_id, image_id)
                scene_object_list = self.load_scene_object_list(scene_id)
                for scene_object_name in scene_object_list:
                    object_id = self.object_id_dict[scene_object_name]
                    instance_mask = mask == object_id
                    bgr[instance_mask] = bgr[instance_mask] // 2 + get_random_color() // 2
                if show:
                    plt.imshow(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
                    plt.show()
                return bgr
            else:
                raise ValueError('The image id must be given for 2d visualization')
        elif dimension == 3:
            geometry_list = []
            if image_id is not None:
                image_pcd = self.load_point_cloud(scene_id, image_id)
                camera_pose = self.load_camera_pose(scene_id, image_id)
                image_pcd.transform(camera_pose)
                geometry_list.append(image_pcd)
            else:
                scene_pcd = self.load_scene_point_cloud(scene_id)
                geometry_list.append(scene_pcd)
            object_pose_dict = self.load_object_pose_dict(scene_id)
            scene_object_list = self.load_scene_object_list(scene_id)
            for scene_object_name in scene_object_list:
                if (scene_object_name in object_pose_dict.keys()) and (object_pose_dict[scene_object_name] is not None):
                    o3d_mesh = self.load_object_mesh(scene_object_name)
                    sixd_pose = object_pose_dict[scene_object_name]
                    o3d_mesh.transform(sixd_pose)
                    geometry_list.append(o3d_mesh.sample_points_uniformly(10000))
            full_pcd = merge_pcds(geometry_list)
            if show:
                o3d.visualization.draw_geometries([full_pcd])
            return full_pcd
        else:
            raise ValueError('Dimension must be 2 or 3')