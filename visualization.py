from cProfile import label
import matplotlib.pyplot as plt
import numpy as np
import cv2

class Visualizer:
    def __init__(self):
        self.fig = plt.figure(figsize=(15, 5))
        self.ax1 = self.fig.add_subplot(1, 3, 1)
        self.ax2 = self.fig.add_subplot(1, 3, 2)
        self.ax3 = self.fig.add_subplot(1, 3, 3, projection='3d')
        plt.ion()
        
    def setup_plots(self):
        self.ax1.set_title('Camera feed')
        self.ax1.axis('off')
        self.ax2.set_title('Camera trajectory (Top view)')
        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Z')
        self.ax2.grid(True)
        self.ax2.axis('equal')
        self.ax3.set_title('3D Map Points')
        self.ax3.set_xlabel('X')
        self.ax3.set_ylabel('Y')
        self.ax3.set_zlabel('Z')
        plt.tight_layout()
        
    def update(self, frame, keypoints, trajectory, map_points, poses):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        self.ax1.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.ax1.set_title(f'Camera feed - Features: {len(keypoints) if keypoints else 0}')
        self.ax1.axis('off')
        
        if len(trajectory) > 1:
            traj_np = np.array(trajectory)
            self.ax2.plot(traj_np[:, 0], traj_np[:, 2], 'b-', lw=2, label='Trajectory')
            self.ax2.plot(traj_np[-1, 0], traj_np[-1, 2], 'ro', ms=8, label='Current position')
            self.ax2.legend()
        self.ax2.set_title(f'Camera Trajectory - Poses: {len(poses)}')
        self.ax2.grid(True)
        self.ax2.axis('equal')
        
        if len(map_points) > 0:
            map_np = np.array(map_points)
            if len(map_np > 1000):
                indices = np.random.choice(len(map_np), size=1000, replace=False)
                map_np = map_np[indices]
            self.ax3.scatter(map_np[:, 0], map_np[:, 1], map_np[:, 2], c='r', s=1)
            
        if len(trajectory) > 1:
            traj_np = np.array(trajectory)
            self.ax3.plot(traj_np[:, 0], traj_np[:, 1], traj_np[:, 2], 'b-', lw=2, label='Trajectory')
            
        self.ax3.set_title(f'3D Map Points - Total: {len(map_points)}')
        plt.draw()
        plt.pause(0.001)
        
    def close(self):
        plt.ioff()
        plt.show()
        