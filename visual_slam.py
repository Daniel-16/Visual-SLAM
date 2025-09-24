from hmac import new
import numpy as np
import cv2
from camera import Camera
from features import FeatureExtractor
from pose_estimation import PoseEstimator
from mapping import Mapper
from visualization import Visualizer

class VisualSLAM:
    def __init__(self):
        self.camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32)
        self.camera = Camera()
        self.feature_extractor = FeatureExtractor()
        self.pose_estimator = PoseEstimator(self.camera_matrix)
        self.mapper = Mapper(self.camera_matrix)
        self.visualizer = Visualizer()
        self.camera_pose = []
        self.trajectory = []
        self.min_matches = 50
        self.prev_frame_color = None
        
    def process_frame(self, frame):
        keypoints, descriptors = self.feature_extractor.detect_and_compute(frame)
        
        if self.feature_extractor.prev_descriptors is None:
            self.feature_extractor.prev_keypoints = keypoints
            self.feature_extractor.prev_descriptors = descriptors
            self.prev_frame_color = frame.copy()
            return frame
        
        matches = self.feature_extractor.match_features(descriptors)
        
        if not matches or len(matches) < self.min_matches:
            self.feature_extractor.prev_keypoints = keypoints
            self.feature_extractor.prev_descriptors = descriptors
            self.prev_frame_color = frame.copy()
            return frame
        
        prev_points, curr_points = self.feature_extractor.extract_matched_points(matches, keypoints)
        R, t = self.pose_estimator.estimate_pose(prev_points, curr_points)
        
        if R is not None and t is not None:
            if not self.camera_pose:
                pose = np.hstack([np.eye(3), np.zeros((3, 1))])
            else:
                prev_pose = self.camera_pose[-1]
                pose = prev_pose @ np.vstack([np.hstack([R, t]), [0, 0, 0, 1]])
                
            self.camera_pose.append(pose)
            self.trajectory.append(pose[:3, 3].flatten())
            new_points = self.mapper.triangulate_points(prev_points, curr_points, R, t)
            self.mapper.add_points_to_map(new_points, pose)
            
        old_keypoints = self.feature_extractor.prev_keypoints
        old_frame = self.prev_frame_color if self.prev_frame_color is not None else frame

        output = cv2.drawMatches(
            old_frame,
            old_keypoints,
            frame,
            keypoints,
            matches[:50],
            None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
        )

        self.feature_extractor.prev_keypoints = keypoints
        self.feature_extractor.prev_descriptors = descriptors
        self.prev_frame_color = frame.copy()
        return output
    
    def run(self):
        print("Visual SLAM started. Move the camera to build a map.")
        print("Press 'q' to quit, 's' to save results.")
        self.visualizer.setup_plots()
        
        try:
            while True:
                frame = self.camera.get_frame()
                if frame is None:
                    break
                
                processed_frame = self.process_frame(frame)
                
                if len(self.camera_pose) % 5 == 0:
                    self.visualizer.update(processed_frame, self.feature_extractor.prev_keypoints, self.trajectory, self.mapper.map_points, self.camera_pose)
                    cv2.imshow('Visual SLAM', processed_frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        self.save_results()
        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            self.visualizer.close()
            
    def save_results(self):
        if self.trajectory:
            np.save('camera_trajectory.npy', np.array(self.trajectory))
            print("Trajectory saved to camera_trajectory.npy")
            
        if self.mapper.map_points:
            np.save('map_points.npy', np.array(self.mapper.map_points))
            print("Map points saved to map_points.npy")