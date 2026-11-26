# ROS 2 integration

This ament Python package provides the live middleware path between a simulator camera topic, OpenVINO inference, optional PX4 SITL telemetry and AgentSON trace recording.

## Build

Use a ROS 2 distribution compatible with the installed Isaac Sim bridge. Install `cv_bridge`, `sensor_msgs`, `std_msgs`, `launch_ros`, OpenVINO, OpenCV and NumPy.

```bash
cd integrations/ros2
rosdep install --from-paths . --ignore-src -r -y
python -m pip install openvino opencv-python-headless numpy
colcon build --symlink-install
source install/setup.bash
```

## Launch the vertical pipeline

Start Isaac Sim with its ROS 2 bridge enabled and publish a camera image as `sensor_msgs/msg/Image` on `/wildfire/sensors/front/image`. Then run:

```bash
ros2 launch wildfire_bridge wildfire_pipeline.launch.py \
  model_path:=/absolute/path/to/model.xml \
  image_topic:=/wildfire/sensors/front/image \
  trace_path:=/absolute/path/to/runs/session.AgentSON
```

The launch starts:
- `status_node`: publishes explicit scaffold/simulation status.
- `inference_node`: subscribes to the image topic and runs a user-supplied OpenVINO model.
- `trace_node`: records status, inference and optional vehicle messages as AgentSON v1.2 observations.

The inference adapter currently reports raw output tensor shapes and latency. It does not decode detections or identify fire/smoke.

## Optional PX4 SITL telemetry

Install `px4_msgs` built from the branch matching the PX4 firmware and run:

```bash
ros2 run wildfire_bridge px4_telemetry_node
```

This adapter is read-only and publishes NED-labelled vehicle state to `/wildfire/vehicle/state`. See [PX4 SITL setup](../px4/ros2-sitl.md).

## Inspect

```bash
ros2 topic list
ros2 topic echo --once /wildfire/simulation/status
ros2 topic echo --once /wildfire/perception/raw
ros2 topic echo --once /wildfire/vehicle/state
```

See the [Isaac Sim bridge contract](../isaac-sim/ros2-bridge.md) and [AgentSON integration profile](../agentson/profiles/wildfire-v1/README.md). Runtime validation still requires the selected local simulator, ROS 2 distribution, OpenVINO model and optional PX4 SITL stack.
