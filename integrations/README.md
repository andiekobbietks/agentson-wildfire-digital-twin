# Integration workspace

This workspace implements the first end-to-end **ROS 2 vertical integration path** for the wildfire demonstrator: a simulator camera publishes ROS 2 images, OpenVINO performs model inference, optional PX4 SITL telemetry is normalised read-only, and an AgentSON recorder captures the pipeline locally.

## Components

| Component | Implemented boundary | External prerequisite / validation |
|---|---|---|
| NVIDIA Isaac Sim | ROS 2 bridge and camera topic contract documented | Isaac Sim, compatible ROS 2 bridge, scene graph and clock must be configured locally |
| ROS 2 | Python package, launch file, status publisher, inference node, trace node | Build with the selected ROS 2 distribution and colcon |
| PX4 SITL | Optional read-only telemetry adapter | PX4 SITL, Micro XRCE-DDS Agent and matching `px4_msgs` |
| OpenVINO | ROS 2 image subscriber and inference publisher | User-supplied static 4D OpenVINO model; no wildfire model included |
| AgentSON | ROS 2 event recorder writing v1.2-shaped session documents | Validate output against the exact upstream schema revision before release |

## Data flow

```text
Isaac Sim camera + /clock
          |
          v
ROS 2 sensor_msgs/Image <----- PX4 SITL (optional, telemetry only)
          |                                |
          v                                v
OpenVINO inference node            PX4 state normaliser
          |                                |
          +---------------+----------------+
                          |
                          v
                  AgentSON trace node
                          |
                          v
              Local .AgentSON session file
```

PX4's standard ROS 2/uXRCE-DDS path is separate from Isaac Sim's ROS bridge. This repository does not claim a native Isaac Sim ↔ PX4 flight-dynamics bridge. If both systems are run together, one simulator must be designated as the vehicle-dynamics authority and clock/state reconciliation must be tested. Do not run two independent physics loops and describe them as one validated simulation.

## Build and run

Use a ROS 2 distribution supported by the selected Isaac Sim release. Install `cv_bridge`, `sensor_msgs`, `std_msgs`, `launch_ros`, OpenCV and OpenVINO in a compatible environment.

```bash
cd integrations/ros2
rosdep install --from-paths . --ignore-src -r -y
python -m pip install openvino opencv-python-headless numpy
colcon build --symlink-install
source install/setup.bash
ros2 launch wildfire_bridge wildfire_pipeline.launch.py \
  model_path:=/absolute/path/to/model.xml \
  image_topic:=/wildfire/sensors/front/image \
  trace_path:=/absolute/path/to/runs/session.AgentSON
```

Isaac Sim or a test publisher must already publish `sensor_msgs/msg/Image` on the configured image topic. The optional PX4 adapter can be run after installing `px4_msgs` built from the branch matching the PX4 firmware:

```bash
ros2 run wildfire_bridge px4_telemetry_node
```

See [Isaac Sim bridge setup](isaac-sim/ros2-bridge.md) and [PX4 SITL telemetry setup](px4/ros2-sitl.md).

## Verification

```bash
ros2 topic list
ros2 topic echo --once /wildfire/simulation/status
ros2 topic echo --once /wildfire/perception/raw
ros2 topic echo --once /wildfire/vehicle/state
```

The vehicle topic is optional. Inspect the generated AgentSON file and validate it against the pinned schema. The current recorder stores source payloads as observation text. It is not a full simulator snapshot and does not provide cryptographic tamper evidence.

## Safety and evidence boundary

- PX4 uXRCE-DDS is unauthenticated; isolate its network and do not expose it to shared/public networks.
- This is simulation-only, read-only PX4 telemetry. Never connect it to a real aircraft.
- Raw model tensors are not fire/smoke detections. A model-specific decoder, model card and independent evaluation are required.
- Do not store raw imagery, credentials, personal data or restricted datasets in traces.
- A successful software pipeline does not validate wildfire spread, emergency response or flight safety.

## Upstream projects

- [NVIDIA Isaac Sim](https://github.com/isaac-sim/IsaacSim)
- [ROS 2](https://github.com/ros2/ros2)
- [PX4 Autopilot](https://github.com/PX4/PX4-Autopilot)
- [OpenVINO](https://github.com/openvinotoolkit/openvino)
- [AgentSON](https://github.com/andiekobbietks/AgentSON)
