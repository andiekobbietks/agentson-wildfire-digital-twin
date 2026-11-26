# AgentSON run records

AgentSON is the local provenance and execution-record layer for the ROS 2 wildfire pipeline. The ROS 2 trace node subscribes to simulation status, OpenVINO inference metadata and optional PX4 telemetry, then appends observations to a session document shaped for AgentSON v1.2.

Upstream canonical schema: [AgentSON v1.2](https://github.com/andiekobbietks/AgentSON/blob/master/spec/v1.2.json). Pin the exact schema revision in any reproducible release and validate generated documents against it.

## Run through ROS 2

The preferred path is the integrated launch file:

```bash
ros2 launch wildfire_bridge wildfire_pipeline.launch.py \
  model_path:=/absolute/path/to/model.xml \
  trace_path:=/absolute/path/to/runs/session.AgentSON
```

The trace recorder listens to:
- `/wildfire/simulation/status`
- `/wildfire/perception/raw`
- `/wildfire/vehicle/state` (optional PX4 SITL telemetry)

The recorder places the topic and source payload in the observation text while retaining the event timestamp, source class, agent and run correlation ID in schema fields. This is deliberately conservative: domain-specific structured semantics belong in a versioned integration profile, not in invented top-level schema properties.

## Limits

The trace proves only that the recorder received and wrote a message. It does not prove that the source telemetry is complete or physically correct, that a model output is a fire detection, or that a simulator reproduces real fire behaviour. The current file writer is local and single-process oriented; concurrent writers, crash recovery, cryptographic signatures and tamper-evident chaining are not yet implemented.
