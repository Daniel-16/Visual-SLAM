import numpy as np
import matplotlib
import os
import sys

DISPLAY = os.environ.get('DISPLAY')
QT_PLATFORM = os.environ.get('QT_QPA_PLATFORM')

backends_to_try = []

if DISPLAY:
    backends_to_try.append(('Qt5Agg', f"Qt5Agg backend with {QT_PLATFORM} platform" if QT_PLATFORM else "Qt5Agg backend"))
    backends_to_try.append(('Agg', "Agg backend (non-interactive)"))
else:
    backends_to_try.append(('Agg', "Agg backend (no DISPLAY available)"))

backend_set = False
for backend_name, description in backends_to_try:
    try:
        matplotlib.use(backend_name)
        print(f"Using {description}")
        backend_set = True
        break
    except ImportError as e:
        print(f"Failed to import {backend_name}: {e}")
        continue

if not backend_set:
    print("All backends failed, using matplotlib default")

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_from_files(trajectory_path='camera_trajectory.npy', map_points_path='map_points.npy'):
    """
    Loads and creates a 3D visualization of a camera trajectory and a point cloud map
    from saved NumPy (.npy) files.

    This function plots the 3D coordinates of the map points as a scatter plot and
    overlays the camera's path as a line plot, including markers for the start
    and end points.

    Args:
        trajectory_path (str): The file path for the saved camera trajectory data.
        map_points_path (str): The file path for the saved 3D map points data.
    """
    try:
        trajectory = np.load(trajectory_path)
        map_points = np.load(map_points_path)
    except FileNotFoundError as e:
        print(f"Error: Could not find a required data file.")
        print(f"Details: {e}")
        print("\nPlease ensure that 'camera_trajectory.npy' and 'map_points.npy' exist")
        print("in the same directory as this script.")
        print("You can generate these files by running the main SLAM program and pressing 's'.")
        return

    if trajectory.size == 0 and map_points.size == 0:
        print("Warning: Both trajectory and map points files are empty. Nothing to plot.")
        return

    print("Data loaded successfully. Generating 3D plot...")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    if map_points.size > 0:
        ax.scatter(map_points[:, 0], map_points[:, 1], map_points[:, 2],
                   c='gray', s=2, alpha=0.5, label='3D Map Points')
    else:
        print("Info: No map points to display.")

    if trajectory.size > 0:
        ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                c='blue', linewidth=2, label='Camera Trajectory')
        ax.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2],
                   c='green', s=100, marker='o', label='Start')
        ax.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2],
                   c='red', s=100, marker='x', label='End')
    else:
        print("Info: No trajectory data to display.")
    
    ax.set_title('Visualization of Saved SLAM Map and Trajectory')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.legend()
    ax.grid(True)
    
    try:
        if map_points.size > 0:
            x_min, x_max = map_points[:, 0].min(), map_points[:, 0].max()
            y_min, y_max = map_points[:, 1].min(), map_points[:, 1].max()
            z_min, z_max = map_points[:, 2].min(), map_points[:, 2].max()
            
            max_range = np.array([x_max-x_min, y_max-y_min, z_max-z_min]).max() / 2.0
            mid_x = (x_max+x_min) * 0.5
            mid_y = (y_max+y_min) * 0.5
            mid_z = (z_max+z_min) * 0.5
            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
    except:
        pass

    backend = matplotlib.get_backend()
    if backend == 'Agg':
        output_file = 'slam_visualization.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file} (no interactive display available)")
    else:
        print("Displaying plot. Close the window to exit the script.")
        plt.show()

if __name__ == "__main__":
    visualize_from_files()