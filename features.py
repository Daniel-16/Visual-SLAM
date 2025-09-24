import cv2
import numpy as np

class FeatureExtractor:
    def __init__(self, n_features=1000):
        self.orb = cv2.ORB_create(nfeatures=n_features)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.prev_keypoints = None
        self.prev_descriptors = None
        
    def detect_and_compute(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.orb.detectAndCompute(gray, None)
    
    def match_features(self, descriptors):
        if self.prev_descriptors is None:
            return None
        matches = self.bf.match(self.prev_descriptors, descriptors)
        return sorted(matches, key=lambda x: x.distance)
    
    def extract_matched_points(self, matches, keypoints):
        prev_points = np.float32([self.prev_keypoints[m.queryIdx].pt for m in matches])
        curr_points = np.float32([keypoints[m.trainIdx].pt for m in matches])
        return prev_points, curr_points
