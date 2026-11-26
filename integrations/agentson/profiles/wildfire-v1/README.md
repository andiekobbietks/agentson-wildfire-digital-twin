# AgentSON Wildfire Integration Profile v1

**Profile identifier:** `agentson-wildfire-v1`  
**Canonical format:** AgentSON v1.2  
**Status:** Initial integration profile for the wildfire demonstrator  
**Compatibility rule:** This profile does not alter the AgentSON v1.2 canonical schema.

## 1. Purpose

The profile gives the wildfire digital-twin integration a small, stable vocabulary for geospatial, simulation, robotics and perception events. It allows different simulator, middleware and inference implementations to emit comparable records without making AgentSON itself specific to wildfire, drones, ROS 2 or OpenVINO.

The profile is a semantic convention layered on the existing AgentSON event model. It is not a new canonical event type and does not introduce unsupported top-level schema properties.

## 2. Encoding rule

Each domain event is stored as a canonical AgentSON `observation` entry. The JSON object below is serialised into the existing `observation.text` string:

```json
{
  "profile": "agentson-wildfire-v1",
  "event_type": "perception.inference.completed",
  "run_id": "scenario-2026-001-run-0001",
  "source_topic": "/wildfire/perception/raw",
  "payload": {
    "model_id": "example-model",
    "latency_ms": 18.4,
    "semantic_interpretation": "not_performed"
  }
}
```

The outer AgentSON entry retains canonical fields such as `type`, `text`, `source`, `agent`, `timestamp`, `correlation_id` and `provenance`. The event object above is a convention inside `text`, not a schema extension.

## 3. Required event envelope

| Field | Requirement | Meaning |
|---|---|---|
| `profile` | Required | Must equal `agentson-wildfire-v1` |
| `event_type` | Required | Namespaced event from the vocabulary below |
| `run_id` | Required | Stable identifier shared by all events in one run |
| `source_topic` | Required for ROS 2 events | Original topic or adapter source |
| `payload` | Required | Event-specific data; preserve original units and frame labels |

Every event should additionally carry a canonical AgentSON timestamp and correlation ID. Use UTC epoch milliseconds for AgentSON entry timestamps. Preserve source/simulation timestamps separately inside the payload when they differ.

## 4. Event vocabulary

| Event type | Producer | Minimum payload |
|---|---|---|
| `scenario.created` | Scenario loader | scenario ID, version, manifest reference |
| `dataset.referenced` | Geospatial/weather adapter | dataset ID, source, licence, retrieval time, CRS or variable units |
| `simulation.initialised` | Isaac Sim adapter | simulator version, scene ID, seed, clock source |
| `simulation.status` | ROS 2 status adapter | component, status, simulator-connected flag |
| `simulation.clock` | Clock adapter | simulation timestamp, epoch/time scale |
| `sensor.frame.received` | Camera adapter | sensor ID, frame ID, source timestamp, encoding, dimensions |
| `robotics.vehicle.state` | PX4/robotics adapter | source, coordinate frame, position/velocity, validity flags, flight state |
| `robotics.failsafe.triggered` | PX4/robotics adapter | source, failsafe code/state, timestamp |
| `perception.inference.completed` | OpenVINO adapter | model ID/hash, runtime/device, input reference, output reference/shape, latency |
| `perception.inference.failed` | OpenVINO adapter | model ID, error type, bounded error description |
| `perception.detection.reported` | Model-specific decoder | class, score semantics, confidence, bounding box/mask reference, frame ID |
| `evaluation.run.completed` | Evaluation adapter | metrics reference, dataset split, limitations |
| `run.completed` | Run orchestrator | outcome, trace reference, manifest reference |

Adapters may add namespaced event types in a profile revision, but must not silently redefine an existing event's meaning.

## 5. Provenance and coordinate conventions

- Label data as `observed`, `reanalysis`, `forecast`, `derived` or `synthetic`; do not collapse these into one generic observation.
- Geospatial payloads must state CRS (prefer an EPSG identifier where valid), horizontal/vertical units, datum and transformation history.
- PX4 local position is NED unless the message contract explicitly states otherwise. Preserve NED labels; never relabel it ENU without applying and recording a transform.
- Preserve simulator/source timestamps and identify the clock authority. Do not replace simulation time with host wall-clock time without recording both.
- Model confidence is meaningful only with the model's score semantics and class mapping. Raw output tensors must not be described as detections.
- Reference large artefacts by URI/path plus digest and metadata; do not embed raw sensor frames or model weights in the trace by default.

## 6. Current implementation mapping

The ROS 2 trace node currently emits:
- `simulation.status` from `/wildfire/simulation/status`;
- the event declared in the inference payload, normally `perception.inference.completed` or `perception.inference.failed`;
- `robotics.vehicle.state` from `/wildfire/vehicle/state`.

The current OpenVINO node emits tensor shapes and latency only. It does not emit `perception.detection.reported`. The PX4 adapter is optional, read-only and requires `px4_msgs` built for the matching PX4 release.

## 7. Conformance

A conforming adapter must:
1. Produce a valid AgentSON v1.2 session document.
2. Keep the profile envelope inside `observation.text` unless a later canonical AgentSON version explicitly defines a better typed representation.
3. Use one stable `run_id` and preserve source timestamps.
4. State units, coordinate frames, source status and uncertainty where relevant.
5. Avoid claims that a trace proves sensor truth, model correctness, physical fire behaviour or operational safety.

The project should pin the exact AgentSON schema commit and run schema validation in CI before describing generated traces as conformant. The current repository integration is a first implementation, not yet an independently verified conformance certification.

## 8. Versioning

Profile revisions are independent of AgentSON canonical versions:
- Profile major: incompatible event meaning or required payload changes.
- Profile minor: additive event types or optional payload fields.
- Profile patch: clarifications and non-semantic corrections.

Do not create AgentSON v1.3 solely to accommodate this domain profile. Promote a concept into the canonical format only if it is broadly useful across domains and has a stable cross-domain semantic definition.
