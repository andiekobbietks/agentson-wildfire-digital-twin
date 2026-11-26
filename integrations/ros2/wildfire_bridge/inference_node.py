"""ROS 2 image subscriber backed by a user-supplied OpenVINO model.

The node emits raw model tensor metadata only. It does not classify fire/smoke.
"""
import json
import time

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from openvino import Core
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class OpenVINOImageNode(Node):
    def __init__(self):
        super().__init__("wildfire_openvino_inference")
        self.declare_parameter("model_path", "")
        self.declare_parameter("device", "AUTO")
        self.declare_parameter("image_topic", "/wildfire/sensors/front/image")
        self.declare_parameter("result_topic", "/wildfire/perception/raw")
        self.declare_parameter("model_id", "user-supplied-model")
        self.declare_parameter("scale", 1.0 / 255.0)
        model_path = self.get_parameter("model_path").value
        if not model_path:
            raise RuntimeError("Set model_path to an OpenVINO IR .xml model")
        core = Core()
        model = core.read_model(model_path)
        self.compiled = core.compile_model(model, self.get_parameter("device").value)
        self.input_port = self.compiled.input(0)
        self.input_shape = list(self.input_port.shape)
        if len(self.input_shape) != 4 or any(not isinstance(d, int) for d in self.input_shape):
            raise RuntimeError(f"Expected a static 4D image input, got {self.input_shape}")
        self.bridge = CvBridge()
        self.scale = float(self.get_parameter("scale").value)
        self.model_id = self.get_parameter("model_id").value
        self.publisher = self.create_publisher(
            String, self.get_parameter("result_topic").value, 10
        )
        self.subscription = self.create_subscription(
            Image, self.get_parameter("image_topic").value, self.on_image, 10
        )
        self.get_logger().info(
            f"OpenVINO ready: model={self.model_id}, input={self.input_shape}"
        )

    def preprocess(self, image):
        shape = self.input_shape
        if shape[1] in (1, 3, 4):
            height, width = shape[2], shape[3]
            resized = cv2.resize(image, (width, height))
            if shape[1] == 1:
                resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)[..., None]
            else:
                resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                if shape[1] == 4:
                    raise ValueError("Four-channel input needs an explicit model adapter")
            tensor = np.transpose(resized, (2, 0, 1))[None, ...]
        else:
            height, width = shape[1], shape[2]
            resized = cv2.cvtColor(cv2.resize(image, (width, height)), cv2.COLOR_BGR2RGB)
            tensor = resized[None, ...]
        return tensor.astype(np.float32) * self.scale

    def on_image(self, message):
        started = time.perf_counter()
        try:
            image = self.bridge.imgmsg_to_cv2(message, desired_encoding="bgr8")
            tensor = self.preprocess(image)
            outputs = self.compiled({self.input_port: tensor})
            latency_ms = (time.perf_counter() - started) * 1000.0
            payload = {
                "event": "perception.inference.completed",
                "semantic_interpretation": "not_performed",
                "model_id": self.model_id,
                "model_path": self.get_parameter("model_path").value,
                "device": self.get_parameter("device").value,
                "source_stamp": {
                    "sec": message.header.stamp.sec,
                    "nanosec": message.header.stamp.nanosec,
                },
                "frame_id": message.header.frame_id,
                "input_shape": self.input_shape,
                "output_shapes": [list(value.shape) for value in outputs.values()],
                "latency_ms": round(latency_ms, 3),
            }
        except Exception as exc:
            payload = {
                "event": "perception.inference.failed",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "frame_id": message.header.frame_id,
            }
        out = String()
        out.data = json.dumps(payload, sort_keys=True)
        self.publisher.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = OpenVINOImageNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
