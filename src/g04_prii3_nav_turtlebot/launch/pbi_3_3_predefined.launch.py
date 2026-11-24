import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, SetEnvironmentVariable


def generate_launch_description():

    home = os.path.expanduser('~')

    workspace = os.path.join(
        home,
        'g04_prii3_ws'
    )

    mapa = os.path.join(
        workspace,
        'src',
        'g04_prii3_nav_turtlebot',
        'maps',
        'f1l3.yaml'
    )

    nodo = os.path.join(
        workspace,
        'src',
        'g04_prii3_nav_turtlebot',
        'g04_prii3_nav_turtlebot',
        'predefined_navigation.py'
    )

    gazebo_models = (
        os.environ.get('GAZEBO_MODEL_PATH', '')
        + ':'
        + os.path.join(
            workspace,
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

    predefined_navigation = TimerAction(
        period=8.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'python3',
                    nodo
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        SetEnvironmentVariable(
            'TURTLEBOT3_MODEL',
            'waffle'
        ),

        SetEnvironmentVariable(
            'GAZEBO_MODEL_PATH',
            gazebo_models
        ),

        gazebo,
        nav2,
        predefined_navigation
    ])
