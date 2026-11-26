"""Minimal ROS 2 heartbeat; reports scaffold status, not simulator telemetry."""

import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimulationStatusNode(Node):
    def __init__(self):
        super().__init__("wildfire_simulation_status")
        self.publisher = self.create_publisher(String, "/wildfire/simulation/status", 10)
        self.timer = self.create_timer(2.0, self.publish_status)
        self.get_logger().info("Publishing scaffold status; no simulator is connected.")

    def publish_status(self):
        message = String()
        message.data = json.dumps(
            {
                "component": "wildfire-digital-twin",
                "status": "scaffold_only",
                "simulator_connected": False,
                "telemetry_validated": False,
            },
            sort_keys=True,
        )
        self.publisher.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = SimulationStatusNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
