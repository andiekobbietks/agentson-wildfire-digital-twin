# AgentSON Wildfire Digital Twin

A research demonstrator exploring a geographically grounded wildfire digital-twin workflow: geospatial and environmental inputs, simulated aerial robotics, perception experiments, and portable AgentSON execution records.

> **Status:** The repository contains a ROS 2 integration path joining a camera image topic, OpenVINO inference, optional read-only PX4 SITL telemetry and AgentSON event recording. A locally validated Isaac Sim scene, a compatible PX4/Isaac shared dynamics bridge, a wildfire-specific model and a physical wildfire-spread model are not included. This remains a research demonstrator, not an operational emergency-response or flight system.

## What this project is

The demonstrator is designed to make scenario inputs, software versions, simulation state, model metadata and pipeline events inspectable. The first vertical slice is intentionally bounded: one simulated camera stream, one user-supplied OpenVINO model, optional PX4 SITL telemetry, and one local AgentSON session record.

### Design principles

- **Geographically grounded:** preserve source, coordinate reference system, resolution, and temporal coverage for terrain and environmental data.
- **Evidence-labelled:** distinguish observations, reanalysis, forecasts, derived values, and synthetic test data.
- **Simulation-first:** use simulated vehicles and controlled scenarios before considering any field activity.
- **Auditable:** record provenance, configuration, events, and limitations in portable AgentSON-compatible traces.
- **Modular:** keep simulation, robotics, geospatial processing, weather ingestion, perception, and event recording loosely coupled.
- **Honest about validation:** a connected software pipeline is not evidence of physical accuracy or operational readiness.

## Integration workspace

The [integration workspace](integrations/README.md) contains:

- [NVIDIA Isaac Sim bridge guide](integrations/isaac-sim/ros2-bridge.md): ROS 2 camera, clock and topic contract.
- [ROS 2 package](integrations/ros2/README.md): status, OpenVINO inference, AgentSON trace and launch entry points.
- [PX4 SITL adapter](integrations/px4/ros2-sitl.md): optional read-only telemetry through ROS 2/uXRCE-DDS.
- [OpenVINO adapter](integrations/openvino/README.md): model runtime and inference constraints.
- [AgentSON integration](integrations/agentson/README.md): local session recording and schema boundary.
- [AgentSON Wildfire integration profile](integrations/agentson/profiles/wildfire-v1/README.md): domain event vocabulary and schema-compatible mapping.

The PX4 and Isaac Sim ROS paths are separate upstream integrations. This repository does not claim they are joined into a single validated physics loop. The full local stack still requires a version-compatible host environment, Isaac Sim scene, PX4 SITL setup and model supplied by the operator.

## MVP sequence

1. Define one documented or explicitly synthetic scenario and source register.
2. Import terrain and map layers with CRS, units, resolution, source and licence metadata.
3. Add time-aligned weather replay with explicit provenance and missing-data handling.
4. Configure a repeatable Isaac Sim scene, camera and simulation clock.
5. Run the ROS 2/OpenVINO/AgentSON vertical pipeline and optionally add PX4 SITL telemetry.
6. Validate the AgentSON output against the pinned schema and package a run bundle.
7. Repeat runs, perturb inputs, measure drift and publish limitations.

## Repository map

- [Product requirements](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Research and data sources](docs/RESEARCH.md)
- [Security and responsible use](docs/SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Integration workspace](integrations/README.md)

## Getting involved

This repository is a research and engineering demonstrator. Open an issue before proposing a major integration, dataset or scope change. Do not upload sensitive personal data, restricted operational information or datasets without checking their terms.

## Validation boundary

A simulator can help test software integration, repeatability and selected behaviours. It cannot by itself establish that a wildfire model predicts real fire spread, that a detector generalises to field conditions, that a drone is safe to fly, or that the system is suitable for emergency-service decision-making. Such claims require separate domain-specific evidence, independent review and appropriate approvals.

## Licence

The source code and documentation in this repository are intended to be released under the Apache License 2.0. Third-party datasets, models, simulator assets and dependencies remain subject to their own licences and terms.
