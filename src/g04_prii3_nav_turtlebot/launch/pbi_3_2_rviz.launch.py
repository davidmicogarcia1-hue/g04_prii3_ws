import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, SetEnvironmentVariable


def generate_launch_description():

    home = os.path.expanduser('~')

    mapa = os.path.join(
        home,
        'g04_prii3_ws',
        'src',
        'g04_prii3_nav_turtlebot',
        'maps',
        'f1l3.yaml'
    )

    gazebo_models = (
        os.environ.get('GAZEBO_MODEL_PATH', '')
        + ':'
        + os.path.join(
            home,
            'g04_prii3_ws',
            'src',
            'f1l3_gazebo',
            'models'
        )
        + ':/opt/ros/humble/share/turtlebot3_gazebo/models'
    )

    gazebo = ExecuteProcess(
        cmd=[
            'ros2',
            'launch',
            'f1l3_gazebo',
            'f1l3_world.launch.py'
        ],
        output='screen'
    )

    nav2 = TimerAction(
        period=3.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2',
                    'launch',
                    'turtlebot3_navigation2',
                    'navigation2.launch.py',
                    'use_sim_time:=True',
                    'map:=' + mapa
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([

        SetEnvironmentVariable(
            'ROS_DOMAIN_ID',
            '44'
        ),

        SetEnvironmentVariable(
            'TURTLEBOT3_MODEL',
            'waffle'
        ),

        SetEnvironmentVariable(
            'GAZEBO_MODEL_PATH',
            gazebo_models
        ),

        gazebo,
        nav2

    ])
