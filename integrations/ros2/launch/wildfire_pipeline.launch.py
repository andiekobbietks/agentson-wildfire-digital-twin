"""Launch the ROS 2 status, OpenVINO and AgentSON pipeline nodes."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    model_path = LaunchConfiguration("model_path")
    trace_path = LaunchConfiguration("trace_path")
    image_topic = LaunchConfiguration("image_topic")
    return LaunchDescription([
        DeclareLaunchArgument("model_path", default_value=""),
        DeclareLaunchArgument("trace_path", default_value="runs/wildfire-session.AgentSON"),
        DeclareLaunchArgument("image_topic", default_value="/wildfire/sensors/front/image"),
        Node(
            package="wildfire_bridge",
            executable="status_node",
            name="wildfire_status",
            output="screen",
        ),
        Node(
            package="wildfire_bridge",
            executable="inference_node",
            name="wildfire_openvino",
            output="screen",
            parameters=[{
                "model_path": model_path,
                "image_topic": image_topic,
                "model_id": "configured-openvino-model",
            }],
        ),
        Node(
            package="wildfire_bridge",
            executable="trace_node",
            name="wildfire_agentson",
            output="screen",
            parameters=[{
                "trace_path": trace_path,
                "topics": [
                    "/wildfire/simulation/status",
                    "/wildfire/perception/raw",
                    "/wildfire/vehicle/state",
                ],
            }],
        ),
    ])
