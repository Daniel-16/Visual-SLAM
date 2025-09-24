import cv2

class Camera:
    def __init__(self, device_id=0):
        self.cap = cv2.VideoCapture(device_id)
        if not self.cap.isOpened():
            raise IOError("Could not open camera. Device ID: {}".format(device_id))
        
    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()