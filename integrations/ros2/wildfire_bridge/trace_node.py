"""Record ROS 2 pipeline events as AgentSON v1.2 observation entries.

The domain event is encoded as JSON inside the canonical observation.text field.
This keeps the adapter compatible with AgentSON v1.2 without inventing schema keys.
"""
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def now_ms():
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def event_type_for(topic, payload):
    if payload.get("event"):
        return payload["event"]
    return {
        "/wildfire/simulation/status": "simulation.status",
        "/wildfire/perception/raw": "perception.inference.completed",
        "/wildfire/vehicle/state": "robotics.vehicle.state",
    }.get(topic, "integration.message.received")


class AgentSONTraceNode(Node):
    def __init__(self):
        super().__init__("wildfire_agentson_trace")
        self.declare_parameter("trace_path", "runs/wildfire-session.AgentSON")
        self.declare_parameter("session_id", "wildfire-session")
        self.declare_parameter("topics", [
            "/wildfire/simulation/status",
            "/wildfire/perception/raw",
            "/wildfire/vehicle/state",
        ])
        self.path = Path(self.get_parameter("trace_path").value)
        self.session_id = self.get_parameter("session_id").value
        if not self.session_id.replace("-", "").replace("_", "").isalnum():
            raise RuntimeError("session_id may contain only letters, digits, _ and -")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.document = self.load_or_create()
        self.subscriptions = []
        for topic in self.get_parameter("topics").value:
            self.subscriptions.append(
                self.create_subscription(
                    String, topic, lambda msg, source=topic: self.record(source, msg), 20
                )
            )
        self.get_logger().info(f"AgentSON trace: {self.path}")

    def load_or_create(self):
        if self.path.exists():
            doc = json.loads(self.path.read_text(encoding="utf-8"))
            if doc.get("id") != self.session_id:
                raise RuntimeError("Existing trace has a different session id")
            return doc
        stamp = now_ms()
        return {
            "$schema": "https://agentson.dev/schema/v1.2.json",
            "id": self.session_id,
            "task": "Wildfire digital-twin simulation run",
            "outcome": "in_progress",
            "tool": {"name": "other", "session_id": self.session_id},
            "started_at": utc_now(),
            "entries": [{
                "type": "stream-meta",
                "stream_id": self.session_id,
                "mode": "single",
                "agents": [{"id": "wildfire-ros2-bridge", "name": "Wildfire ROS 2 integration"}],
                "agent": "wildfire-ros2-bridge",
                "timestamp": stamp,
                "provenance": {"confidence": "confirmed", "source": "system"},
            }],
        }

    def record(self, topic, message):
        try:
            payload = json.loads(message.data)
        except json.JSONDecodeError:
            payload = {"text": message.data}
        event_type = event_type_for(topic, payload)
        event_document = {
            "profile": "agentson-wildfire-v1",
            "event_type": event_type,
            "run_id": self.session_id,
            "source_topic": topic,
            "payload": payload,
        }
        entry = {
            "type": "observation",
            "text": json.dumps(event_document, sort_keys=True, separators=(",", ":")),
            "source": "sensor" if "sensor" in topic or "perception" in topic else "system",
            "agent": "wildfire-ros2-bridge",
            "timestamp": now_ms(),
            "correlation_id": self.session_id,
            "provenance": {"confidence": "confirmed", "source": "system"},
        }
        with self.lock:
            self.document["entries"].append(entry)
            self.document["heartbeat"] = utc_now()
            temp = self.path.with_suffix(self.path.suffix + ".tmp")
            temp.write_text(
                json.dumps(self.document, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            os.replace(temp, self.path)


def main(args=None):
    rclpy.init(args=args)
    node = AgentSONTraceNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
