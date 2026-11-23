import os

from glob import glob
from setuptools import find_packages, setup


package_name = 'g04_prii3_nav_turtlebot'


setup(

    name=package_name,

    version='0.0.0',

    packages=find_packages(
        exclude=['test']
    ),

    data_files=[

        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),

        (
            'share/' + package_name,
            ['package.xml']
        ),

        # Ficheros launch
        (
            os.path.join(
                'share',
                package_name,
                'launch'
            ),

            glob('launch/*.launch.py')
        ),

        # Mapas
        (
            os.path.join(
                'share',
                package_name,
                'maps'
            ),

            glob('maps/*')
        ),
    ],

    install_requires=[
        'setuptools'
    ],

    zip_safe=True,

    maintainer='david',

    maintainer_email='davidmicogarcia1@gmail.com',

    description=(
        'Navegacion autonoma del TurtleBot3 '
        'para el proyecto PRII3'
    ),

    license='TODO: License declaration',

    extras_require={
        'test': [
            'pytest',
        ],
    },

    entry_points={

        'console_scripts': [

            'predefined_navigation = '
            'g04_prii3_nav_turtlebot.'
            'predefined_navigation:main',

            'aruco_destination = '
            'g04_prii3_nav_turtlebot.'
            'aruco_destination:main',

            'autonomous_navigation = '
            'g04_prii3_nav_turtlebot.'
            'autonomous_navigation:main',

        ],

    },

)
