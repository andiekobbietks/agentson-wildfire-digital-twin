# PX4 SITL telemetry into the wildfire ROS 2 graph

This integration is intentionally **read-only**. It consumes PX4 SITL telemetry and normalises selected fields for recording. It does not send offboard commands, arm, take off, or control a vehicle.

## Compatibility requirements

- Run PX4 SITL with the simulator target and PX4 release selected in the compatibility matrix.
- Build/install `px4_msgs` from the branch corresponding to that PX4 release.
- Start the Micro XRCE-DDS Agent when required by the selected PX4 setup.
- Keep the DDS network isolated. PX4 documents that uXRCE-DDS exposes uORB topics and that the transport is unauthenticated; do not bridge it onto a shared or public network.
- Confirm topic names and message definitions against the exact PX4 build before enabling the adapter.

PX4 documentation: https://docs.px4.io/main/en/ros2/user_guide and https://docs.px4.io/main/en/middleware/uxrce_dds

## Run

Build the ROS 2 package after installing `px4_msgs` for the matching firmware:

```bash
cd integrations/ros2
colcon build --symlink-install
source install/setup.bash
ros2 run wildfire_bridge px4_telemetry_node
```

The adapter subscribes to `/fmu/out/vehicle_status_v1` and `/fmu/out/vehicle_local_position`, then publishes a normalised JSON message to `/wildfire/vehicle/state`. It preserves NED axis labels and validity flags. It does not convert NED to ENU; any consumer requiring ENU must apply and record an explicit transform.

This is SITL-only research software. Do not connect the adapter to a real aircraft.
