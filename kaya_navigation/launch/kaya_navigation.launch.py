import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_share = get_package_share_directory("kaya_navigation")

    use_sim_time = LaunchConfiguration("use_sim_time", default="True")

    map_dir = LaunchConfiguration(
        "map",
        default=os.path.join(pkg_share, "maps", "KayaMap.yaml")
    )

    param_dir = LaunchConfiguration(
        "params_file",
        default=os.path.join(pkg_share, "config", "kaya_nav2_params.yaml")
    )

    nav2_bringup_dir = os.path.join(
        get_package_share_directory("nav2_bringup"),
        "launch"
    )

    return LaunchDescription([

        DeclareLaunchArgument("map", default_value=map_dir),
        DeclareLaunchArgument("params_file", default_value=param_dir),
        DeclareLaunchArgument("use_sim_time", default_value="True"),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, "bringup_launch.py")
            ),
            launch_arguments={
                "map": map_dir,
                "use_sim_time": use_sim_time,
                "params_file": param_dir,
                "use_docking": "False",   # 🔥 THIS disables docking server completely
            }.items(),
        ),



        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            remappings=[
                ('cloud_in', ['/lidar_points']),
                ('scan', ['/scan'])
            ],
            parameters=[{
                'target_frame': 'base_link',
                'transform_tolerance': 0.01,
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
            name='pointcloud_to_laserscan'
        )
    ])

