# Isaac Sim to ROS 2 bridge

This is the simulator-facing half of the vertical integration. Isaac Sim remains an external installation; no proprietary simulator binary or asset is vendored here.

## Required runtime setup

1. Install an Isaac Sim release and follow its matching ROS 2 bridge documentation.
2. Use a ROS 2 distribution supported by that exact Isaac Sim release. Source the ROS environment before starting Isaac Sim, or use the ROS libraries bundled with the selected Isaac Sim release as NVIDIA documents.
3. Enable the `isaacsim.ros2.bridge` extension.
4. Create a camera in the scene and publish its image as `sensor_msgs/msg/Image` on `/wildfire/sensors/front/image`. Publish `sensor_msgs/msg/CameraInfo` on `/wildfire/sensors/front/camera_info` when calibration is available.
5. Set the simulation clock consistently. If ROS nodes use simulated time, publish `/clock` and set `use_sim_time=true` on all participating nodes.
6. Confirm the ROS 2 graph and inspect the image encoding, frame ID, dimensions, and timestamp before starting inference.

## Topic contract

| Topic | Type | Producer | Consumer |
|---|---|---|---|
| `/clock` | `rosgraph_msgs/msg/Clock` | Isaac Sim clock publisher | ROS 2 nodes |
| `/wildfire/sensors/front/image` | `sensor_msgs/msg/Image` | Isaac Sim camera | OpenVINO node |
| `/wildfire/simulation/status` | `std_msgs/msg/String` | status node | AgentSON trace node |
| `/wildfire/perception/raw` | `std_msgs/msg/String` | OpenVINO node | AgentSON trace node |
| `/wildfire/vehicle/state` | `std_msgs/msg/String` | optional PX4 adapter | AgentSON trace node |

The OpenVINO node currently records raw tensor shapes and latency only. It deliberately does not label output tensors as fire or smoke. A model-specific decoder and model card are required before semantic detections can be emitted.

## Verification

With Isaac Sim running and the camera graph active:

```bash
ros2 topic list
ros2 topic echo --once /clock
ros2 topic info /wildfire/sensors/front/image
ros2 topic hz /wildfire/sensors/front/image
```

Then inspect one image message and confirm the header timestamp advances with simulation time. The ROS 2 bridge is not considered validated until this check and an image-to-inference smoke test pass on the pinned host stack.

Official documentation: https://docs.isaacsim.omniverse.nvidia.com/latest/ros2_tutorials/index.html
