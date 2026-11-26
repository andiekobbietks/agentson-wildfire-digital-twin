"""Append an integration event to a local AgentSON v1.2 session document."""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--component", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--detail", default="")
    parser.add_argument("--session-id", default=None)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    session_id = args.session_id or re.sub(r"[^A-Za-z0-9_-]", "-", output.stem)
    if not session_id or not re.match(r"^[A-Za-z0-9_-]+$", session_id):
        parser.error("session id must contain only letters, numbers, underscore or hyphen")

    if output.exists():
        document = json.loads(output.read_text(encoding="utf-8"))
        if document.get("id") != session_id:
            parser.error("existing file belongs to a different session; use --session-id to match")
    else:
        document = {
            "$schema": "https://agentson.dev/schema/v1.2.json",
            "id": session_id,
            "task": "Wildfire digital-twin integration experiment",
            "outcome": "in_progress",
            "tool": {"name": "other", "session_id": session_id},
            "started_at": utc_now(),
            "entries": [
                {
                    "type": "stream-meta",
                    "stream_id": session_id,
                    "mode": "single",
                    "agents": [{"id": "wildfire-integration", "name": "Wildfire integration adapter"}],
                    "agent": "wildfire-integration",
                    "timestamp": timestamp,
                    "provenance": {"confidence": "confirmed", "source": "system"},
                }
            ],
        }

    event_text = args.detail or f"{args.component}: {args.event}"
    document["entries"].append(
        {
            "type": "observation",
            "text": event_text,
            "source": "system",
            "agent": "wildfire-integration",
            "timestamp": timestamp,
            "provenance": {"confidence": "confirmed", "source": "system"},
        }
    )
    document["heartbeat"] = utc_now()
    output.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {output}")


if __name__ == "__main__":
    main()
