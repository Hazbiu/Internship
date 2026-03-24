ls /opt/ros
source /opt/ros/humble/setup.bash
ros2 node list
./launch-slam_toolbox.sh
cd ~/github/Internship/zero-to-slam/scripts
./ros2-container.sh bash
clear
exit
pwd
cd scripts
ls
ls
clear
source /opt/ros/humble/setup.bash
ros2 topic list
ros2 run pointcloud_to_laserscan pointcloud_to_laserscan_node   --ros-args   -r cloud_in:=/front_3d_lidar/lidar_points   -r scan:=/scan
apt update
apt install ros-humble-pointcloud-to-laserscan
sudo apt update
sudo apt update
exit
pwd
source /opt/ros/humble/setup.bash
ros2 topic list | grep scan
ros2 topic echo /front_2d_lidar/scan
ros2 topic list | grep scan
ros2 topic list
echo $ROS_DOMAIN_ID
clear
ros2 topic list | grep scan
ros2 topic echo /front_2d_lidar/scan
ros2 topic list | grep scan
+ros2 launch slam_toolbox online_async_launch.py scan_topic:=/front_2d_lidar/scan
./ros2-container.sh bash
source /opt/ros/humble/setup.bash
ros2 topic list | grep map
exit
cd ~/github/Internship/zero-to-slam/scripts
./ros2-container.sh bash
cd ~/github/Internship/zero-to-slam/scripts
./ros2-container.sh bash
exit
ros2 topic echo /map
ros2 topic info /map
ros2 topic hz /map
ros2 run rviz2 rviz2
exit
pwd
source /opt/ros/humble/setup.bash
ros2 launch slam_toolbox online_async_launch.py scan_topic:=/front_2d_lidar/scan
exit
