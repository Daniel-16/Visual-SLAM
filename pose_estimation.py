import cv2
import numpy as np

class PoseEstimator:
    def __init__(self, camera_matrix):
        self.camera_matrix = camera_matrix
    
    def estimate_pose(self, prev_points, curr_points):
        E, mask = cv2.findEssentialMat(curr_points, prev_points, self.camera_matrix, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        if E is None:
            return None, None
        
        _, R, t, mask = cv2.recoverPose(E, curr_points, prev_points, self.camera_matrix)
        return R, t