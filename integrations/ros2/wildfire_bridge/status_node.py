"""Publish pipeline status and observe whether a sensor stream is arriving."""
import json
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class SimulationStatusNode(Node):
    def __init__(self):
        super().__init__("wildfire_simulation_status")
        self.declare_parameter("image_topic", "/wildfire/sensors/front/image")
        self.declare_parameter("stale_after_seconds", 5.0)
        self.publisher = self.create_publisher(String, "/wildfire/simulation/status", 10)
        self.last_frame_monotonic = None
        self.frame_count = 0
        self.image_subscription = self.create_subscription(
            Image, self.get_parameter("image_topic").value, self.on_image, 10
        )
        self.timer = self.create_timer(2.0, self.publish_status)
        self.get_logger().info("Monitoring the configured sensor topic; simulator identity is not inferred.")

    def on_image(self, _message):
        self.last_frame_monotonic = time.monotonic()
        self.frame_count += 1

    def publish_status(self):
        stale_after = float(self.get_parameter("stale_after_seconds").value)
        active = (
            self.last_frame_monotonic is not None
            and time.monotonic() - self.last_frame_monotonic <= stale_after
        )
        message = String()
        message.data = json.dumps(
            {
                "component": "wildfire-digital-twin",
                "status": "sensor_stream_active" if active else "awaiting_sensor_stream",
                "sensor_stream_active": active,
                "sensor_frames_received": self.frame_count,
                "simulator_identity_verified": False,
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
