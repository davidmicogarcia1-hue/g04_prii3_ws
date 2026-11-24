# PRII3 - Grupo 04

Proyecto realizado para la asignatura **Proyecto RII 3: Robots Inteligentes**.

## Integrantes

- David Micó García
- Carlos Villar Cejalvo
- Marcos Anaya Benavente

---

# Requisitos generales

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- colcon
- OpenCV
- Navigation2
- TurtleBot3

## Descargar el proyecto

```bash
git clone https://github.com/davidmicogarcia1-hue/g04_prii3_ws.git
cd g04_prii3_ws
```

## Compilar el workspace

```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

Cada vez que se abra una terminal nueva:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
source ~/.bashrc
```

---

# Configuración ROS_DOMAIN_ID

Para evitar interferencias con otros grupos se utiliza:

```text
ROS_DOMAIN_ID=157
```

Se configura una sola vez en `~/.bashrc`:

```bash
echo 'export ROS_DOMAIN_ID=157' >> ~/.bashrc
source ~/.bashrc
```

Para comprobarlo:

```bash
echo $ROS_DOMAIN_ID
```

Debe aparecer:

```text
157
```

El ordenador y el robot deben utilizar el mismo `ROS_DOMAIN_ID`.

---

# Sprint 1 - Turtlesim

## Paquete

```text
g04_prii3_turtlesim
```

Se utiliza `turtlesim` para realizar un movimiento autónomo que dibuja el número del grupo:

```text
04
```

## Ejecutar

```bash
ros2 launch g04_prii3_turtlesim dibujo04.launch.py
```

## Servicios

Detener:

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

Reanudar:

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

Reiniciar:

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

---

# Sprint 2

En el Sprint 2 se trabaja con:

- JetBot real
- TurtleBot3 Waffle en simulación

Paquetes:

```text
g04_prii3_move_jetbot
g04_prii3_move_turtlebot
```

Los dos implementan:

```text
draw_number
collision_avoidance
```

---

# Sprint 2 - TurtleBot3 en simulación

Seleccionar TurtleBot3 Waffle:

```bash
export TURTLEBOT3_MODEL=waffle
```

Abrir Gazebo:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

## Draw Number

```bash
ros2 run g04_prii3_move_turtlebot draw_number
```

El TurtleBot realiza automáticamente:

```text
04
```

## Collision Avoidance

```bash
ros2 run g04_prii3_move_turtlebot collision_avoidance
```

El nodo utiliza:

```text
/scan
```

Cuando detecta un obstáculo:

```text
TurtleBot → se detiene
```

Cuando desaparece:

```text
TurtleBot → continúa
```

---

# Sprint 2 - JetBot real

## Conexión

El ordenador y el JetBot deben encontrarse en la misma red.

```bash
ssh jetbot@IP_DEL_ROBOT
```

También se puede utilizar VS Code Remote-SSH.

Workspace del JetBot:

```text
/home/jetbot/ros2_ws
```

## Preparación

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/.bashrc
```

## Draw Number

```bash
ros2 run g04_prii3_move_jetbot draw_number
```

## Collision Avoidance

```bash
ros2 run g04_prii3_move_jetbot collision_avoidance
```

El LiDAR utiliza:

```text
/scan
```

---

# Sprint 3 - Navegación

El Sprint 3 implementa navegación y localización utilizando:

- Gazebo
- RViz
- Navigation2
- AMCL
- LiDAR
- Cámara
- OpenCV
- Marcadores ArUco

Paquete principal de simulación:

```text
g04_prii3_nav_turtlebot
```

Se han implementado:

```text
PBI 3.2 - Navegación guiada mediante RViz
PBI 3.3 - Navegación predefinida
PBI 3.4 - Navegación autónoma mediante ArUco
```

---

# Preparación de la simulación

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
source ~/.bashrc
```

Comprobar dominio:

```bash
echo $ROS_DOMAIN_ID
```

Debe devolver:

```text
157
```

Seleccionar modelo:

```bash
export TURTLEBOT3_MODEL=waffle
```

Añadir modelos de Gazebo:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/g04_prii3_ws/src/f1l3_gazebo/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

---

# PBI 3.2 - Navegación guiada mediante RViz

Launch:

```text
pbi_3_2_rviz.launch.py
```

Ejecutar:

```bash
ros2 launch g04_prii3_nav_turtlebot pbi_3_2_rviz.launch.py
```

En RViz:

1. Seleccionar `2D Pose Estimate`.
2. Indicar posición y orientación inicial.
3. Seleccionar `Nav2 Goal`.
4. Marcar una pose destino.
5. Navigation2 calcula la trayectoria.
6. El robot navega hasta el objetivo.

Flujo:

```text
RViz
 ↓
2D Pose Estimate
 ↓
AMCL
 ↓
Robot localizado
 ↓
Nav2 Goal
 ↓
Navigation2
 ↓
TurtleBot3
```

---

# AMCL

AMCL permite estimar dónde está el robot dentro del mapa.

Intervienen:

```text
/map
/scan
/initialpose
/amcl_pose
```

La pose inicial se publica en:

```text
/initialpose
```

Tipo:

```text
geometry_msgs/msg/PoseWithCovarianceStamped
```

AMCL publica su estimación mediante:

```text
/amcl_pose
```

Conceptualmente:

```text
Mapa + LiDAR + odometría
          ↓
         AMCL
          ↓
Posición estimada
```

AMCL responde:

```text
¿Dónde está el robot?
```

Navigation2 responde:

```text
¿Cómo llegar al destino?
```

---

# PBI 3.3 - Navegación predefinida

Nodo:

```text
predefined_navigation
```

Archivo:

```text
predefined_navigation.py
```

Launch:

```text
pbi_3_3_predefined.launch.py
```

Ejecutar:

```bash
ros2 launch g04_prii3_nav_turtlebot pbi_3_3_predefined.launch.py
```

El nodo lleva al TurtleBot desde una pose inicial predefinida en el pasillo hasta una pose final predefinida dentro del laboratorio.

## Pose inicial

```text
x = -0.6283862590789795
y = -5.823587417602539
gamma = -0.014495306414798126
```

## Pose final

```text
x = 2.169
y = 8.444
gamma = 1.332
```

El funcionamiento es:

```text
Pose inicial predefinida
        ↓
/initialpose
        ↓
AMCL
        ↓
Robot localizado
        ↓
NavigateToPose
        ↓
Pose final predefinida
```

El nodo utiliza:

```text
/amcl_pose
/initialpose
navigate_to_pose
```

La navegación se realiza automáticamente sin seleccionar el destino manualmente desde RViz.

---

# PBI 3.4 - Navegación autónoma

La navegación autónoma utiliza:

```text
autonomous_navigation
aruco_destination
```

Secuencia:

```text
Pose inicial
     ↓
AMCL localiza
     ↓
Navegación hasta la puerta
     ↓
Detección de ArUco
     ↓
Selección del destino
     ↓
Navegación hasta la pose final
```

---

# autonomous_navigation

Está suscrito a:

```text
/amcl_pose
/destino_aruco
```

Publica:

```text
/initialpose
```

Utiliza:

```text
nav2_msgs/action/NavigateToPose
```

mediante:

```text
navigate_to_pose
```

El nodo:

1. Publica la pose inicial.
2. Espera a AMCL.
3. Navega hasta la puerta.
4. Espera un destino procedente del detector ArUco.
5. Envía ese destino a Navigation2.
6. Navega hasta la pose final.

---

# aruco_destination

Está suscrito a:

```text
/camera/image_raw
```

Tipo:

```text
sensor_msgs/msg/Image
```

La imagen se convierte a OpenCV mediante:

```text
CvBridge
```

Después se detecta el marcador ArUco y se obtiene su ID.

---

# Destinos ArUco

IDs utilizados:

```text
5
6
17
```

## ID 5

```text
x = -3.3882179278364295
y = 1.833430544730172
gamma = 2.8143108387285256
```

## ID 6

```text
x = -3.2033594467599604
y = 7.641596806469504
gamma = -2.54057856469949
```

## ID 17

```text
x = 2.169
y = 8.444
gamma = 1.332
```

El ArUco proporciona el ID.

Las coordenadas se obtienen mediante:

```text
DESTINOS[id_aruco]
```

---

# /destino_aruco

El nodo `aruco_destination` publica:

```text
/destino_aruco
```

Tipo:

```text
geometry_msgs/msg/Pose2D
```

Contiene:

```text
x
y
theta
```

Flujo:

```text
/camera/image_raw
        ↓
aruco_destination
        ↓
ID ArUco
        ↓
DESTINOS[id]
        ↓
/destino_aruco
        ↓
autonomous_navigation
        ↓
NavigateToPose
        ↓
Navigation2
```

---

# Ejecución de navegación autónoma

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
source ~/.bashrc
```

```bash
export TURTLEBOT3_MODEL=waffle
```

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/g04_prii3_ws/src/f1l3_gazebo/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

Ejecutar:

```bash
ros2 launch g04_prii3_nav_turtlebot autonomous_demo.launch.py
```

---

# Topics principales del Sprint 3

```text
/map
/scan
/initialpose
/amcl_pose
/camera/image_raw
/destino_aruco
/cmd_vel
```

Tipos:

```text
/map
nav_msgs/msg/OccupancyGrid
```

```text
/scan
sensor_msgs/msg/LaserScan
```

```text
/initialpose
geometry_msgs/msg/PoseWithCovarianceStamped
```

```text
/amcl_pose
geometry_msgs/msg/PoseWithCovarianceStamped
```

```text
/camera/image_raw
sensor_msgs/msg/Image
```

```text
/destino_aruco
geometry_msgs/msg/Pose2D
```

```text
/cmd_vel
geometry_msgs/msg/Twist
```

Acción:

```text
navigate_to_pose
nav2_msgs/action/NavigateToPose
```

---

# Sprint 3 - JetBot físico

Workspace:

```text
/home/jetbot/ros2_ws
```

Dominio:

```text
ROS_DOMAIN_ID=157
```

El PC y el JetBot deben estar en la misma red.

## Nodo base

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/.bashrc

ros2 run jetbot_pro_ros2 jetbot
```

## LiDAR

```bash
ros2 run rplidar_ros rplidar_composition --ros-args \
-p serial_port:=/dev/ttyACM1 \
-p serial_baudrate:=115200 \
-p frame_id:=laser_frame
```

Publica:

```text
/scan
```

## TF LiDAR

```bash
ros2 run tf2_ros static_transform_publisher \
0 0 0.15 3.14 0 0 \
base_link laser_frame
```

Cadena:

```text
odom
 ↓
base_link
 ↓
laser_frame
```

---

# Mapa físico

Archivos:

```text
/home/jetbot/map.yaml
/home/jetbot/map.pgm
```

Ejecutar:

```bash
ros2 run nav2_map_server map_server --ros-args \
-p yaml_filename:=/home/jetbot/map.yaml \
-p use_sim_time:=false
```

Activar:

```bash
ros2 lifecycle set /map_server configure
ros2 lifecycle set /map_server activate
```

---

# AMCL físico

```bash
ros2 run nav2_amcl amcl --ros-args \
-p use_sim_time:=false \
--params-file ~/ros2_ws/jetbot_pro_ros2/param/nav.yaml
```

Activar:

```bash
ros2 lifecycle set /amcl configure
ros2 lifecycle set /amcl activate
```

AMCL está suscrito a:

```text
/initialpose
/map
/scan
```

y publica:

```text
/amcl_pose
/tf
```

---

# RViz físico

En el PC:

```bash
source ~/.bashrc
source /opt/ros/humble/setup.bash

rviz2 -d ~/nav2.rviz
```

Mapa:

```text
Resolución: 0.05 m/píxel
Tamaño: 546 x 540
```

---

# Estructura principal del workspace

```text
g04_prii3_ws/
│
├── src/
│   ├── g04_prii3_turtlesim/
│   ├── g04_prii3_move_turtlebot/
│   ├── g04_prii3_move_jetbot/
│   ├── g04_prii3_nav_turtlebot/
│   │   ├── launch/
│   │   │   ├── autonomous_demo.launch.py
│   │   │   ├── pbi_3_2_rviz.launch.py
│   │   │   └── pbi_3_3_predefined.launch.py
│   │   ├── maps/
│   │   └── g04_prii3_nav_turtlebot/
│   │       ├── autonomous_navigation.py
│   │       ├── aruco_destination.py
│   │       └── predefined_navigation.py
│   │
│   └── f1l3_gazebo/
│
├── .gitignore
└── README.md
```

Las carpetas:

```text
build/
install/
log/
```

no deben almacenarse en Git.
