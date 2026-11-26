# ROS 2 integration

This folder contains a small ROS 2 Python package scaffold for exchanging status/event messages. It intentionally uses standard message types until the sensor and vehicle interfaces are selected.

## Build

Run inside an environment with a supported ROS 2 distribution and `colcon` installed:

```bash
cd integrations/ros2
colcon build --symlink-install
source install/setup.bash
ros2 run wildfire_bridge status_node
```

The node publishes a heartbeat on `/wildfire/simulation/status`. It does not connect to Isaac Sim or PX4 yet.

## Next interface decisions

1. Pin a ROS 2 distribution against the selected Isaac Sim bridge release.
2. Define message contracts for simulation clock, vehicle state, camera metadata and inference results.
3. Standardise units, frames (including ENU/NED conversion), timestamps and coordinate reference handling.
4. Add QoS, timeout and stale-data behaviour before connecting live sensor streams.
