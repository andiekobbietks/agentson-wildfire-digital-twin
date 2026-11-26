# AgentSON run records

AgentSON is the local provenance and execution-record layer for the ROS 2 wildfire pipeline. The ROS 2 trace node subscribes to simulation status, OpenVINO inference metadata and optional PX4 telemetry, then appends observations to a session document shaped for AgentSON v1.2.

Upstream canonical schema: [AgentSON v1.2](https://github.com/andiekobbietks/AgentSON/blob/master/spec/v1.2.json). Pin the exact schema commit in reproducible releases.

## Integration profile

The [AgentSON Wildfire Integration Profile v1](profiles/wildfire-v1/README.md) defines namespaced domain events while preserving the canonical v1.2 schema. Event payloads are serialised into `observation.text`; canonical entry fields retain timestamps, source, agent, correlation ID and provenance.

## Validate a trace

Install the validator dependency:

```bash
python -m pip install -r integrations/agentson/requirements.txt
python integrations/agentson/validate_trace.py \
  --trace runs/session.AgentSON \
  --schema path/to/AgentSON/spec/v1.2.json
```

The validator checks the supplied schema and the profile envelope/run ID. It does not certify semantic truth or completeness of source telemetry.

## Limits

The trace proves only that the recorder received and wrote a message. It does not prove that source telemetry is complete or physically correct, that a model output is a fire detection, or that a simulator reproduces real fire behaviour. The current file writer is local and single-process oriented; concurrent writers, crash recovery, cryptographic signatures and tamper-evident chaining are not implemented.
