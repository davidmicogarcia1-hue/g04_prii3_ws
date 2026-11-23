import os

from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    TimerAction,
    SetEnvironmentVariable
)

from launch_ros.actions import Node


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
        + ':/opt/ros/humble/share/'
        'turtlebot3_gazebo/models'
    )


    # -----------------------------------------------------
    # GAZEBO
    # -----------------------------------------------------

    gazebo = ExecuteProcess(
        cmd=[
            'ros2',
            'launch',
            'f1l3_gazebo',
            'f1l3_world.launch.py'
        ],
        output='screen'
    )


    # -----------------------------------------------------
    # NAVIGATION 2
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # NAVEGACIÓN AUTÓNOMA
    #
    # Arranca pronto.
    # Si AMCL todavía no está preparado,
    # seguirá publicando la pose inicial.
    # -----------------------------------------------------

    navegacion = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='g04_prii3_nav_turtlebot',
                executable='autonomous_navigation',
                name='autonomous_navigation',
                output='screen',
                parameters=[
                    {'use_sim_time': True}
                ]
            )
        ]
    )


    # -----------------------------------------------------
    # RVIZ
    # LO DEJAMOS COMO ESTABA
    # -----------------------------------------------------

    rviz = TimerAction(
        period=7.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'bash',
                    '-c',
                    'LIBGL_ALWAYS_SOFTWARE=1 '
                    'rviz2 '
                    '-d /opt/ros/humble/share/nav2_bringup/'
                    'rviz/nav2_default_view.rviz '
                    '--ros-args -p use_sim_time:=true'
                ],
                output='screen'
            )
        ]
    )


    # -----------------------------------------------------
    # DETECTOR DE ARUCOS
    # -----------------------------------------------------

    detector = TimerAction(
        period=10.0,
        actions=[
            Node(
                package='g04_prii3_nav_turtlebot',
                executable='aruco_destination',
                name='aruco_destination',
                output='screen',
                parameters=[
                    {'use_sim_time': True}
                ]
            )
        ]
    )


    # -----------------------------------------------------
    # LANZAMIENTO COMPLETO
    # -----------------------------------------------------

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
        nav2,
        navegacion,
        rviz,
        detector

    ])
