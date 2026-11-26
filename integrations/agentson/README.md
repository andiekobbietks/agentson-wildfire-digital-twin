# AgentSON run records

AgentSON is the provenance and execution-record layer for this demonstrator. The integration writes a session document with a stream header and observations for scenario metadata and component events.

Upstream canonical schema: [AgentSON v1.2](https://github.com/andiekobbietks/AgentSON/blob/master/spec/v1.2.json). AgentSON is currently alpha/pre-release; pin and validate against the exact schema revision used by your deployment.

## Usage

```bash
python integrations/agentson/record_event.py \
  --output runs/example.AgentSON \
  --component ros2 \
  --event scaffold_started \
  --detail "ROS 2 status node launched"
```

Each invocation creates or appends to a local JSON document. Treat all sensor frames, prompts, model outputs and geospatial references as potentially sensitive. Redact before recording and avoid placing credentials or raw personal data in event details.

The trace is evidence of what this adapter was told or observed. It does not prove the completeness or correctness of upstream telemetry, model predictions, fire behaviour, or operational outcomes.
