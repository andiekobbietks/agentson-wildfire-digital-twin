# PX4 Software-in-the-Loop (SITL)

PX4 SITL is intended for flight-controller and vehicle-behaviour experiments without a physical aircraft.

Upstream: https://github.com/PX4/PX4-Autopilot

## Separate baseline

Follow the official PX4 developer guide to install its toolchain and simulator dependencies. From a PX4-Autopilot checkout, a common Gazebo SITL target is:

```bash
make px4_sitl gz_x500
```

Exact targets and dependencies vary by PX4 release. Use the official guide for the version you select.

## Boundary

This baseline is not an Isaac Sim integration. PX4's Gazebo SITL path and NVIDIA Isaac Sim are separate simulator environments. Connecting PX4 to Isaac Sim requires a compatible transport/bridge, matching message definitions, clock synchronisation, frame transforms and safety tests. None are asserted as implemented here.

Never connect this research scaffold to a real aircraft. Do not use it for operational wildfire response or flight planning.
