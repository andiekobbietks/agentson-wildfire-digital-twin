from setuptools import setup

package_name = "wildfire_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Wildfire Digital Twin maintainers",
    maintainer_email="maintainers@example.invalid",
    description="ROS 2 interface scaffold for the wildfire digital twin.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "status_node = wildfire_bridge.status_node:main",
        ],
    },
)
