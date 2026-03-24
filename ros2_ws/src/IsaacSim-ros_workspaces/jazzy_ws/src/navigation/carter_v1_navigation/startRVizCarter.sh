#!/bin/bash

echo "===== Sourcing ROS 2 Jazzy ====="
source /opt/ros/jazzy/setup.bash

echo "===== Cleaning workspace ====="
cd ~/ros2_ws || exit 1
rm -rf build install log

echo "===== Building workspace ====="
cd ~/ros2_ws/src/IsaacSim-ros_workspaces/jazzy_ws || exit 1
colcon build --symlink-install

echo "===== Sourcing workspace ====="
source install/setup.bash

echo "===== Starting Nav2 for Carter v1 ====="
ros2 launch carter_v1_navigation carter_v1_navigation.launch.py
