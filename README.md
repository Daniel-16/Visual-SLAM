# Visual SLAM

A complete Visual SLAM (Simultaneous Localization and Mapping) implementation using OpenCV, NumPy, and Matplotlib. This repository provides a working monocular SLAM pipeline with camera capture, feature extraction and matching, relative pose estimation, point triangulation, and both live and offline visualization.

## Features

- **Complete SLAM Pipeline**: Full implementation in `visual_slam.py` with proper state management
- **Camera capture**: Simple wrapper over OpenCV `VideoCapture` (`camera.py`)
- **Features**: ORB keypoints, Hamming BFMatcher, and helpers to extract matched tracks (`features.py`)
- **Pose estimation**: Essential matrix (RANSAC) + pose recovery (`pose_estimation.py`)
- **Mapping**: Linear triangulation and world-point accumulation (`mapping.py`)
- **Live Visualization**: Real-time 2D trajectory and 3D map point display (`visualization.py`)
- **Offline Visualization**: Standalone 3D map viewer for saved data (`view_map.py`)
- **Data Persistence**: Save/load camera trajectories and map points as NumPy arrays


## Requirements

- Python >= 3.8
- Linux/macOS/Windows with a working webcam (for live demo)

Core dependencies (managed in `pyproject.toml`):

- `opencv-python>=4.8.0`
- `numpy>=1.24.0`
- `matplotlib>=3.7.0`
- `PyQt5>=5.15.0` (for interactive matplotlib backends)

Dev (optional): `pytest`, `black`, `flake8`.

## Installation

You can use `uv` (recommended for speed) or plain `pip`.

### Using uv

```bash
# install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# from folder root
uv init
uv sync
```

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
```

## Usage

### Running the SLAM System

```bash
# Run the complete SLAM pipeline
uv run main.py

# Or directly:
uv run visual_slam.py
```

**Controls during SLAM:**

- Press `'q'` to quit
- Press `'s'` to save current trajectory and map points to `.npy` files
- Press `'r'` to reset the system

### Viewing Saved Data

```bash
# View saved trajectory and map points in 3D
uv run view_map.py
```

This will load `camera_trajectory.npy` and `map_points.npy` (if they exist) and display them in an interactive 3D plot.

### Data Files

The system automatically saves data to:

- `camera_trajectory.npy`: Camera poses as 4x4 transformation matrices
- `map_points.npy`: 3D world points as Nx3 arrays

## Module Overview

### Core SLAM Components

- **`visual_slam.VisualSLAM`**: Main SLAM pipeline orchestrator

  - `run()`: Main execution loop with keyboard controls
  - `process_frame(frame)`: Process individual camera frames
  - Handles state management, feature tracking, and visualization

- **`camera.Camera`**: Camera interface

  - `get_frame()`: Capture frames from webcam
  - `release()`: Clean up camera resources

- **`features.FeatureExtractor`**: Feature detection and matching

  - `detect_and_compute(frame)`: ORB keypoints/descriptors
  - `match_features(descriptors)`: BFMatcher cross-checked matches
  - `extract_matched_points(matches, keypoints)`: Returns aligned point pairs

- **`pose_estimation.PoseEstimator`**: Camera pose estimation

  - `estimate_pose(prev_points, curr_points)`: Essential matrix (RANSAC) + recoverPose → `(R, t)`

- **`mapping.Mapper`**: 3D point mapping
  - `triangulate_points(prev_points, curr_points, R, t)`: Linear triangulation
  - `add_points_to_map(new_points, pose)`: Transform to world coordinates and accumulate

### Visualization Components

- **`visualization.Visualizer`**: Live visualization during SLAM

  - `setup_plots()`: Initialize matplotlib plots
  - `update(frame, keypoints, trajectory, map_points, poses)`: Update displays
  - `close()`: Clean up visualization

- **`view_map.py`**: Standalone 3D map viewer
  - `visualize_from_files()`: Load and display saved trajectory and map data
  - Supports both interactive display and file export
  - Robust backend selection for different environments

## Technical Notes

- **Camera Calibration**: For best results, use a calibrated camera and update the camera matrix in `visual_slam.py`
- **Scale**: This implementation lacks scale estimation; the map scale is arbitrary
- **Robustness**: This is an educational implementation; production SLAM systems include additional features like:
  - Robust initialization procedures
  - Loop closure detection
  - Bundle adjustment
  - Keyframe management
  - Scale estimation
  - Dense mapping

## Development

- Format: `black .`
- Lint: `flake8`
- Test: `pytest` (if/when tests are added)

## Environment Setup

For systems with display issues (common in headless environments or certain Linux distributions):

1. Set environment variables in your `.env` file:

   ```bash
   export QT_QPA_PLATFORM=xcb
   export DISPLAY=:0  # or your display number
   ```

2. The visualization system will automatically:
   - Try Qt5Agg backend for interactive displays
   - Fall back to saving plots as PNG files if no interactive backend is available

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
