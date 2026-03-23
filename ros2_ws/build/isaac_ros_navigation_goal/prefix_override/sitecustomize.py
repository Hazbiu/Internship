import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/hazbiu/ros2_ws/install/isaac_ros_navigation_goal'
