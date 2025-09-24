import cv2
import numpy as np

class Mapper:
    def __init__(self, camera_matrix):
        self.camera_matrix = camera_matrix
        self.map_points = []
        
    def triangulate_points(self, prev_points, curr_points, R, t):
        P1 = self.camera_matrix @ np.hstack((np.eye(3), np.zeros((3, 1))))
        P2 = self.camera_matrix @ np.hstack([R.T, -R.T @ t])
        
        points_4d = cv2.triangulatePoints(P1, P2, prev_points.T, curr_points.T)
        points_3d = points_4d[:3] / points_4d[3]
        
        valid_points = [p for p in points_3d.T if 0 < p[2] < 100]
        return np.array(valid_points)
    
    def add_points_to_map(self, new_points, pose):
        if len(new_points) > 0:
            world_points = (pose[:3, :3] @ new_points.T + pose[:3, 3:4]).T
            self.map_points.extend(world_points)