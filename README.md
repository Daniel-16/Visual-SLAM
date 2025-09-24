# Visual SLAM

A minimal Visual SLAM (Simultaneous Localization and Mapping) playground using OpenCV, NumPy, and Matplotlib. The repository provides building blocks for a monocular SLAM pipeline: camera capture, feature extraction and matching, relative pose estimation, point triangulation, and simple live visualization.

## Features

- **Camera capture**: simple wrapper over OpenCV `VideoCapture` (`camera.py`).
- **Features**: ORB keypoints, Hamming BFMatcher, and helpers to extract matched tracks (`features.py`).
- **Pose estimation**: Essential matrix (RANSAC) + pose recovery (`pose_estimation.py`).
- **Mapping**: linear triangulation and basic world-point accumulation (`mapping.py`).
- **Visualization**: live 2D trajectory and 3D map point scatter (`visualization.py`).
<!-- 
## Project structure

```
slam-project/
  ├─ camera.py            # Camera wrapper
  ├─ features.py          # ORB features + BFMatcher utilities
  ├─ pose_estimation.py   # Essential matrix + recoverPose
  ├─ mapping.py           # Triangulation + naive map
  ├─ visualization.py     # Matplotlib live views
  ├─ main.py              # Placeholder entrypoint
  ├─ visual_slam.py       # (reserved for future pipeline orchestration)
  ├─ pyproject.toml       # Project metadata and dependencies
  ├─ uv.lock              # Lockfile (if using `uv`)
  ├─ LICENSE              # MIT
  └─ README.md            # This file 
```
-->

## Requirements

- Python >= 3.8
- Linux/macOS/Windows with a working webcam (for live demo)

Core dependencies (managed in `pyproject.toml`):

- `opencv-python>=4.8.0`
- `numpy>=1.24.0`
- `matplotlib>=3.7.0`

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

Notes:

- For best results, use a calibrated camera and set `fx, fy, cx, cy` accordingly.
- This is a minimal, educational pipeline; it lacks many production SLAM features (robust initialization, scale estimation, loop closure, keyframe management, bundle adjustment, etc.).

## Module overview

- `camera.Camera`: opens a webcam, provides `get_frame()` and `release()`.
- `features.FeatureExtractor`:
  - `detect_and_compute(frame)`: ORB keypoints/descriptors.
  - `match_features(descriptors)`: BFMatcher cross-checked matches to previous frame.
  - `extract_matched_points(matches, keypoints)`: returns aligned `prev_points, curr_points`.
- `pose_estimation.PoseEstimator`:
  - `estimate_pose(prev_points, curr_points)`: Essential matrix (RANSAC) and `recoverPose` → `(R, t)`.
- `mapping.Mapper`:
  - `triangulate_points(prev_points, curr_points, R, t)`: linear triangulation.
  - `add_points_to_map(new_points, pose)`: transform to world and accumulate.
- `visualization.Visualizer`:
  - `setup_plots()`, `update(frame, keypoints, trajectory, map_points, poses)`, `close()`.

## Development

- Format: `black .`
- Lint: `flake8`
- Test: `pytest` (if/when tests are added)

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
