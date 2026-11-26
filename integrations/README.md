# Integration workspace

This directory contains adapters and reproducible integration scaffolding for the wildfire digital-twin demonstrator. It does **not** vendor upstream simulator, flight-stack, middleware, or inference-engine source code.

## Components

| Component | Role here | Integration status |
|---|---|---|
| [NVIDIA Isaac Sim](isaac-sim/README.md) | 3D environment, sensor and robot simulation | Setup and interface boundary documented; scene extension not yet validated |
| [ROS 2](ros2/README.md) | Middleware between simulation, vehicle and perception adapters | Minimal Python package scaffold |
| [PX4 SITL](px4/README.md) | Software-in-the-loop flight-controller experiments | Separate SITL launch scaffold; Isaac bridge is not claimed |
| [OpenVINO](openvino/README.md) | Local inference against a user-supplied model | Generic image inference adapter; no wildfire model included |
| [AgentSON](agentson/README.md) | Portable run and event record | Local trace writer targeting the AgentSON v1.2 document shape |

## Data flow (intended)

```text
Terrain + weather inputs
          |
          v
  Isaac Sim environment <----> ROS 2 topics
                                  |
                         PX4 SITL (separate
                         compatibility gate)
                                  |
                           camera / sensor
                                  |
                                  v
                       OpenVINO model adapter
                                  |
                                  v
                       AgentSON run record
```

The PX4/Isaac Sim transport path is deliberately not represented as working. Validate simulator versions, ROS 2 distribution, PX4 release, DDS bridge and coordinate/time conventions before connecting them.

## Local development

- Read each component README before installing dependencies.
- Keep simulator installations external to this repository. Isaac Sim and PX4 have substantial platform and GPU requirements.
- Use a dedicated Python environment for OpenVINO and another environment/container matching the selected ROS 2 distribution.
- Do not commit simulator binaries, model weights, real incident imagery, credentials, or restricted geospatial datasets.
- Record model identity, input provenance, confidence/score semantics, timestamps and failure states. A detector output is not a verified fire observation.

## Upstream projects

- [NVIDIA Isaac Sim](https://github.com/isaac-sim/IsaacSim)
- [ROS 2](https://github.com/ros2/ros2)
- [PX4 Autopilot](https://github.com/PX4/PX4-Autopilot)
- [OpenVINO](https://github.com/openvinotoolkit/openvino)
- [AgentSON](https://github.com/andiekobbietks/AgentSON)

Each upstream project retains its own licence, release cadence and installation requirements. This repository's Apache-2.0 licence does not relicense third-party components or assets.
