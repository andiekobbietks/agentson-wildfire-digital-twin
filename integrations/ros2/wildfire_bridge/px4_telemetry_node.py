"""Optional, read-only PX4 SITL telemetry normaliser.

Requires px4_msgs built for the matching PX4 release. This node does not
publish commands and must not be connected to a real aircraft.
"""
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from px4_msgs.msg import VehicleStatus
    from px4_msgs.msg import VehicleLocalPosition
except ImportError as exc:
    raise RuntimeError(
        "px4_msgs is required. Build the message package matching your PX4 release."
    ) from exc


class PX4TelemetryNode(Node):
    def __init__(self):
        super().__init__("wildfire_px4_telemetry")
        self.publisher = self.create_publisher(String, "/wildfire/vehicle/state", 10)
        self.status = None
        self.position = None
        self.create_subscription(
            VehicleStatus, "/fmu/out/vehicle_status_v1", self.on_status, 10
        )
        self.create_subscription(
            VehicleLocalPosition, "/fmu/out/vehicle_local_position", self.on_position, 10
        )

    def on_status(self, message):
        self.status = message
        self.publish_state()

    def on_position(self, message):
        self.position = message
        self.publish_state()

    def publish_state(self):
        if self.status is None or self.position is None:
            return
        payload = {
            "event": "robotics.vehicle.state",
            "source": "px4_sitl",
            "read_only": True,
            "navigation_state": int(self.status.nav_state),
            "arming_state": int(self.status.arming_state),
            "failsafe": bool(self.status.failsafe),
            "local_position_ned_m": {
                "north": float(self.position.x),
                "east": float(self.position.y),
                "down": float(self.position.z),
            },
            "velocity_ned_mps": {
                "north": float(self.position.vx),
                "east": float(self.position.vy),
                "down": float(self.position.vz),
            },
            "xy_valid": bool(self.position.xy_valid),
            "z_valid": bool(self.position.z_valid),
            "v_xy_valid": bool(self.position.v_xy_valid),
            "v_z_valid": bool(self.position.v_z_valid),
            "timestamp_us": int(self.position.timestamp),
            "coordinate_frame": "NED",
        }
        message = String()
        message.data = json.dumps(payload, sort_keys=True)
        self.publisher.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = PX4TelemetryNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
