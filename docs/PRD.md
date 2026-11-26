# Product Requirements Document

**Project:** AgentSON Wildfire Digital Twin  
**Status:** Draft, research demonstrator  
**Owner:** AndieKobbieTech / Andrea Kwabena Technologies  
**Repository:** `andiekobbietks/agentson-wildfire-digital-twin`

## 1. Executive summary

Build a reproducible, geographically grounded simulation demonstrator for exploring how terrain, historical weather, simulated aerial robotics, perception software, and auditable agent workflows can be brought together around a bounded wildfire scenario.

The product is a research and engineering platform. It is not an operational command system, a replacement for emergency services, a certified flight system, or a validated fire-behaviour forecasting product.

## 2. Problem and opportunity

Wildfire technology demonstrations can be difficult to assess when their geographic inputs, environmental assumptions, model versions, and agent actions are not traceable. A useful demonstrator should make those elements explicit, replayable, and inspectable.

The project investigates whether a modular digital-twin workflow can:
- reconstruct a bounded scenario from documented geospatial and environmental sources;
- replay time-aligned weather inputs into a simulation;
- exercise a simulated aerial platform and perception pipeline;
- preserve event provenance and execution history in portable records;
- evaluate repeatability, robustness, and limitations.

## 3. Goals

1. Produce one repeatable scenario based on a documented incident or clearly labelled synthetic scenario.
2. Preserve geospatial coordinate systems, units, resolution, source dates, and licences.
3. Replay a bounded historical weather window with explicit missing-data handling.
4. Integrate one simulated aerial vehicle and one sensor/perception pipeline.
5. Emit a complete AgentSON-compatible trace for each run.
6. Publish reproducible setup instructions, evaluation results, and known limitations.

## 4. Non-goals

- Real-world autonomous flight or beyond-visual-line-of-sight operations.
- Dispatching or directing emergency responders.
- Predicting real fire spread without a separately validated physical model.
- Replacing AEMET, emergency-service systems, incident command, or official warnings.
- Training on personal, restricted, or unlicensed imagery.
- Claiming improved detection lead time or lives/property saved without a valid evaluation design.
- Treating visual fire or smoke effects in a renderer as a physical fire simulation.

## 5. Users and stakeholders

| Persona | Need |
|---|---|
| Simulation engineer | Reproducible scene, inputs, and deterministic run configuration |
| Robotics engineer | Clear interfaces for simulated vehicle, sensors, and middleware |
| Geospatial researcher | CRS-aware terrain and source provenance |
| ML/perception engineer | Repeatable inputs, model metadata, latency and error evaluation |
| Reviewer / auditor | Understand what data and software produced a result |
| Emergency-management domain expert | Review assumptions and identify unsafe interpretations |

## 6. MVP scope

**Included**
- One bounded geographic area and one scenario timeline.
- Terrain and map layer ingestion with metadata.
- One historical weather replay adapter.
- One Isaac Sim scene, subject to hardware and licensing feasibility.
- ROS 2 integration and PX4 SITL only after a version compatibility test.
- One camera/perception path using a replaceable inference adapter.
- AgentSON run manifest and event trace.
- A small evaluation suite and reproducibility instructions.

**Deferred**
- Multiple drones, multi-agent coordination, live feeds, operational alerting, online data fusion, and real-world field trials.
- Coupled physics-based wildfire spread modelling until a suitable model, inputs, and validation plan are selected.

## 7. Functional requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| FR-001 | Every scenario has a unique ID and versioned manifest. | Manifest validates against schema. |
| FR-002 | Record scenario name, geographic extent, time window, and authoring date. | Required fields present. |
| FR-003 | Record CRS/EPSG or explicit CRS definition for each spatial layer. | Import report includes CRS. |
| FR-004 | Record source, licence, retrieval date, spatial resolution, and temporal coverage. | Data register complete. |
| FR-005 | Reject or explicitly flag unknown coordinate reference systems. | Test fixture demonstrates rejection/flag. |
| FR-006 | Convert units only through documented transformations. | Unit conversion tests pass. |
| FR-007 | Distinguish observed, reanalysis, forecast, derived, and synthetic values. | Data status present in metadata. |
| FR-008 | Preserve missing values; do not silently interpolate. | Missing-data test passes. |
| FR-009 | Weather replay is aligned to a documented simulation clock. | Timestamp alignment report. |
| FR-010 | Wind inputs are mapped to the intended simulation interface explicitly. | Integration test and mapping note. |
| FR-011 | Environmental inputs and any fire model remain separate modules. | Architecture and interface test. |
| FR-012 | A rendered fire/smoke effect is labelled visual-only unless physically modelled. | UI and documentation state limitation. |
| FR-013 | Scene configuration is versioned and reproducible. | Same config can be reloaded. |
| FR-014 | Simulated vehicle identity and configuration are recorded. | Run manifest contains vehicle metadata. |
| FR-015 | ROS 2 topics and message types are documented. | Interface inventory. |
| FR-016 | PX4 SITL integration is gated on tested version compatibility. | Compatibility matrix entry. |
| FR-017 | Simulation is visibly distinguished from real telemetry. | UI labels and event metadata. |
| FR-018 | Sensor frames carry timestamps and coordinate-frame metadata. | Frame validation tests. |
| FR-019 | Perception model name, version, hash, and runtime are recorded. | Inference event metadata. |
| FR-020 | Detection outputs retain confidence and class metadata. | Structured output sample. |
| FR-021 | Evaluation includes false positives and false negatives where labels exist. | Evaluation report. |
| FR-022 | Latency is measured on the actual test hardware. | Benchmark report with hardware details. |
| FR-023 | Model output is never represented as ground truth. | Documentation and UI wording. |
| FR-024 | Each run receives a unique run ID. | Run manifest and trace agree. |
| FR-025 | Record software versions and configuration hashes. | Trace metadata complete. |
| FR-026 | Record source references for external datasets. | Provenance event present. |
| FR-027 | Record state transitions and key actions in AgentSON events. | Trace inspection confirms sequence. |
| FR-028 | Trace integrity checks can detect modification. | Tamper test. |
| FR-029 | Trace integrity is not presented as proof that source data is true. | Security documentation. |
| FR-030 | Buffer events locally during simulated network interruption. | Offline/reconnect test. |
| FR-031 | Reconnection does not silently reorder or overwrite events. | Sequence/integrity test. |
| FR-032 | Export a run bundle with manifest, trace, and evaluation outputs. | Bundle can be independently inspected. |
| FR-033 | Runs can be repeated from a pinned manifest. | Repeat-run comparison. |
| FR-034 | Document expected nondeterminism and tolerances. | Reproducibility note. |
| FR-035 | Provide an explicit compatibility matrix for simulator, middleware, and autopilot. | Matrix updated per release. |
| FR-036 | Fail clearly when required assets or datasets are absent. | Missing-asset test. |
| FR-037 | Keep secrets and credentials out of source control. | Secret scanning / review. |
| FR-038 | Document third-party licence obligations. | Licence register. |
| FR-039 | Include a safety and misuse boundary in public documentation. | README and security guide. |
| FR-040 | No real-world flight or emergency response integration without a separate approval gate. | Change-control record. |

## 8. Quality attributes

- **Reproducibility:** manifests, pinned versions, hashes, deterministic seeds where supported.
- **Portability:** avoid coupling event records to a single simulator or inference provider.
- **Observability:** structured logs, run IDs, timestamps, and diagnostic reports.
- **Integrity:** immutable source references and tamper-evident trace handling.
- **Interoperability:** explicit schemas and versioned adapters.
- **Maintainability:** modular components and documented compatibility constraints.
- **Responsible use:** visible distinction between simulation, evidence, and operational claims.

## 9. User stories

- As a simulation engineer, I can load a versioned scenario so another engineer can reproduce the same setup.
- As a geospatial researcher, I can inspect each layer's CRS, licence, resolution, and source.
- As a robotics engineer, I can replay weather and sensor inputs against a simulated vehicle.
- As an ML engineer, I can compare detector outputs against labelled data and report failure cases.
- As a reviewer, I can inspect a portable event trace and understand how a result was produced.

## 10. Evaluation plan

| Area | Initial measure | Important caveat |
|---|---|---|
| Geospatial | CRS validity, alignment error, resolution metadata | Does not establish survey-grade accuracy |
| Weather | Timestamp coverage, missingness, unit validation | Reanalysis is not a local sensor observation |
| Simulation | Frame rate, simulation-time drift, repeatability | Renderer performance is not model validity |
| Robotics | Message latency, dropped messages, state consistency | SITL is not a flight safety case |
| Perception | Precision, recall, false-positive rate, latency | Requires representative labelled evaluation data |
| Trace | Event completeness, schema validity, integrity checks | Integrity does not establish truth |
| Resilience | Recovery time, event loss, ordering after reconnect | Tested only under defined fault injection |

## 11. Risks and mitigations

- **Version incompatibility:** maintain a tested matrix; do not assume latest versions interoperate.
- **Hardware constraints:** start with a minimal scene and benchmark before expanding; document GPU/VRAM requirements.
- **Data licensing:** review each dataset and asset licence before redistribution.
- **Geographic misalignment:** validate CRS, units, vertical datum, and coordinate transforms.
- **False confidence:** label synthetic data and visual effects; publish limitations beside results.
- **Model bias / domain shift:** evaluate across conditions and disclose dataset coverage.
- **Network interruption:** local buffering, sequence numbers, integrity checks, and explicit recovery tests.
- **Scope expansion:** keep the first milestone to one scenario and one simulated vehicle.

## 12. Definition of done for MVP

- A documented scenario manifest and source register exist.
- Terrain and weather inputs load with validated metadata.
- A single simulated vehicle and sensor path execute in the scene.
- One perception adapter produces timestamped outputs.
- One AgentSON trace captures the run and validates against the selected schema.
- A run bundle can be exported and inspected.
- Repeated runs and at least three fault/edge cases are reported.
- Documentation states what has and has not been validated.
