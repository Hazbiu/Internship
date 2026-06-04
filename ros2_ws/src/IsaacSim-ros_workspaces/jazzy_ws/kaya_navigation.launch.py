import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time", default="True")

    kaya_nav_dir = get_package_share_directory("kaya_navigation")
    nav2_bringup_dir = get_package_share_directory("nav2_bringup")

    map_file = os.path.join(kaya_nav_dir, "maps", "KayaMap.yaml")
    params_file = os.path.join(kaya_nav_dir, "config", "kaya_nav2_params.yaml")
    rviz_config = os.path.join(kaya_nav_dir, "rviz", "kaya_navigation.rviz")

    pointcloud_to_scan = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        output='screen',
        remappings=[
            ('cloud_in', '/lidar_points'),
            ('scan', '/scan')
        ],
        parameters=[{
            'target_frame': 'base_link',
            'transform_tolerance': 0.05,
            'min_height': -0.4,
            'max_height': 1.5,
            'angle_min': -1.57,
            'angle_max': 1.57,
            'angle_increment': 0.0087,
            'scan_time': 0.3333,
            'range_min': 0.05,
            'range_max': 30.0,
            'use_inf': True,
            'inf_epsilon': 1.0,
            'use_sim_time': True,
        }],
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "map": map_file,
            "use_sim_time": use_sim_time,
            "params_file": params_file,
            "use_docking": "false",
        }.items(),
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "rviz_launch.py")
        ),
        launch_arguments={
            "rviz_config": rviz_config,
        }.items(),
    )

    return LaunchDescription([

        # start lidar conversion first
        pointcloud_to_scan,

        # start nav2 after TF + scan ready
        TimerAction(
            period=6.0,
            actions=[nav2_launch]
        ),

        # start rviz after nav2
        TimerAction(
            period=10.0,
            actions=[rviz_launch]
        ),
    ])
