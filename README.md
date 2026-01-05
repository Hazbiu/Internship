# Installation of Isaac Sim 5.1.0

## Go to link provided below and follow the steps:

https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/quick-install.html


## ⚠️ Caution

If you will use a conda environment, make sure that the python version you are using matches with the python version of ROS2 that you will use.

---

# Installation of the ROS2 Jazzy

The following packages are required:

```bash
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
sudo apt install ros-jazzy-turtlebot3*
```

---

# How to get the rqt graph?

Run the command listed below:

```bash
ros2 run rqt_graph rqt_graph
```
---
# ROS 2 topic publisher

Below are listed the command to move the robot in doffrent directions.

## Move forward

Run the command listed below:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.3, y: 0.0}, angular: {z: 0.0}}"
```

## Rotate in place

Run the command listed below:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0, y: 0.0}, angular: {z: 0.6}}"
```

## Move sideways

Run the command listed below:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0, y: 0.0}, angular: {z: 0.6}}"
```
---

# How to use teleop?

Run the command listed below:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
---
