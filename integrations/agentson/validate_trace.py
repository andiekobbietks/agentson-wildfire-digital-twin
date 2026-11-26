"""Validate an AgentSON session against a caller-supplied canonical schema."""
import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


PROFILE = "agentson-wildfire-v1"


def validate_profile_envelopes(document):
    errors = []
    for index, entry in enumerate(document.get("entries", [])):
        if entry.get("type") != "observation":
            continue
        text = entry.get("text", "")
        try:
            envelope = json.loads(text)
        except (TypeError, json.JSONDecodeError):
            continue
        if envelope.get("profile") != PROFILE:
            continue
        for key in ("event_type", "run_id", "source_topic", "payload"):
            if key not in envelope:
                errors.append(f"entries[{index}].text: missing profile field {key}")
        if envelope.get("run_id") != document.get("id"):
            errors.append(f"entries[{index}].text: run_id does not match session id")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace", required=True, help="AgentSON session JSON file")
    parser.add_argument("--schema", required=True, help="Local AgentSON v1.2 JSON Schema file")
    args = parser.parse_args()
    trace = json.loads(Path(args.trace).read_text(encoding="utf-8"))
    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(trace), key=lambda error: list(error.path))
    errors.extend(validate_profile_envelopes(trace))
    if errors:
        for error in errors:
            print(f"INVALID: {error}")
        raise SystemExit(1)
    print(f"VALID: {args.trace} conforms to the supplied AgentSON schema and profile envelope checks")


if __name__ == "__main__":
    main()
