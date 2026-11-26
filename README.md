# AgentSON Wildfire Digital Twin

A research and engineering project for a geographically grounded wildfire digital-twin demonstrator. The project brings together terrain and geospatial data, historical weather replay, simulated aerial robotics, perception experiments, and **AgentSON** execution records.

> **Status:** Research scaffold. This repository does not currently contain a validated wildfire-spread model, operational drone system, or clinically/operationally validated emergency-response capability.

## What this project is

The intended demonstrator will reconstruct a bounded wildfire scenario in a digital environment and make the inputs, assumptions, simulation state, and agent actions inspectable. The initial target is one documented incident, one terrain area, one simulated drone, one weather replay, one perception pipeline, and one complete AgentSON trace.

### Design principles

- **Geographically grounded:** preserve source, coordinate reference system, resolution, and temporal coverage for terrain and environmental data.
- **Evidence-labelled:** distinguish observations, reanalysis, forecasts, derived values, and synthetic test data.
- **Simulation-first:** use simulated vehicles and controlled scenarios before considering any field activity.
- **Auditable:** record provenance, configuration, events, and limitations in portable AgentSON-compatible traces.
- **Modular:** keep simulation, robotics, geospatial processing, weather ingestion, perception, and event recording loosely coupled.
- **Honest about validation:** visual plausibility is not evidence of physical accuracy or operational readiness.

## Proposed architecture

| Layer | Candidate technologies | Responsibility |
|---|---|---|
| Geospatial foundation | IGN/CNIG, Copernicus, GIS tooling | Terrain, boundaries, map layers, coordinate metadata |
| Environmental replay | ERA5 / Copernicus CDS, AEMET where available | Time-aligned historical weather inputs |
| Simulation | NVIDIA Isaac Sim | Scene, sensors, environment, simulated robot |
| Robotics | ROS 2, PX4 SITL | Messaging, vehicle and autonomy integration in simulation |
| Perception | OpenVINO and replaceable model adapters | Local inference experiments and measured outputs |
| Event governance | AgentSON | Portable execution records, provenance, integrity and audit trail |
| Evaluation | Reproducible scenarios and metrics | Compare runs and document uncertainty |

These are candidate components, not a claim that every integration is already implemented or mutually compatible. Versions and interfaces must pass a compatibility gate before being pinned.

## MVP sequence

1. **Scenario definition:** choose one documented incident and define a bounded area, timeline, and evidence register.
2. **Geospatial baseline:** import terrain and map layers while preserving CRS, units, resolution, and licence.
3. **Weather replay:** ingest a small time window and label every field by source and data status.
4. **Simulation baseline:** create one scene and one simulated aerial vehicle; verify coordinate and clock alignment.
5. **Perception baseline:** connect one camera stream to a replaceable detector and record latency and failure cases.
6. **AgentSON trace:** capture scenario configuration, source references, state transitions, inference metadata, and run outcomes.
7. **Evaluation:** repeat runs, perturb inputs, measure drift, and publish limitations.

## Repository map

- [Product requirements](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Research and data sources](docs/RESEARCH.md)
- [Security and responsible use](docs/SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## Getting involved

This repository is currently a design and research scaffold. Please open an issue before proposing a major integration, dataset, or scope change. Do not upload sensitive personal data, restricted operational information, or datasets without checking their terms.

## Validation boundary

A simulator can help test software integration, repeatability, and selected behaviours. It cannot by itself establish that a wildfire model predicts real fire spread, that a detector generalises to field conditions, that a drone is safe to fly, or that the system is suitable for emergency-service decision-making. Any such claims require separate domain-specific evidence, independent review, and appropriate approvals.

## Licence

The source code and documentation in this repository are intended to be released under the Apache License 2.0. Third-party datasets, models, simulator assets, and dependencies remain subject to their own licences and terms.
