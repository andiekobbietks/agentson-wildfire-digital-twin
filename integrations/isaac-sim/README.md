# NVIDIA Isaac Sim

Isaac Sim is the intended 3D scene, sensor and robot simulation environment. Install it separately using NVIDIA's official instructions: https://docs.isaacsim.omniverse.nvidia.com/

## Intended responsibilities

- Load a bounded, documented terrain scene and preserve its coordinate reference metadata.
- Configure a simulated aerial platform and camera/sensor suite.
- Publish simulation time and sensor outputs through a version-matched ROS 2 integration.
- Support repeatable scenarios with explicit seeds and configuration snapshots.

## Current status

This repository does not yet include a validated wildfire scene, terrain importer, aircraft asset, ROS 2 bridge configuration, or Isaac Sim extension. Do not interpret the architecture diagram as proof of a working Isaac Sim ↔ PX4 connection.

## Compatibility gate

Before implementing the bridge, record the exact Isaac Sim release, host OS, GPU/driver, ROS 2 distribution, Python version, bridge extension version, coordinate convention and simulation clock source. Run a minimal scene and one sensor publisher first.

Keep proprietary or separately licensed assets outside the repository unless their terms explicitly permit redistribution.
