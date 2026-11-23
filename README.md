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

En este Sprint se utiliza `turtlesim` para realizar un movimiento autónomo que dibuja el número del grupo:

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

## Preparación

Si TurtleBot3 no está instalado:

```bash
sudo apt install ros-humble-turtlebot3*
```

Seleccionar TurtleBot3 Waffle:

```bash
export TURTLEBOT3_MODEL=waffle
```

Abrir Gazebo:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

En otra terminal:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
source ~/.bashrc
```

## Draw Number

Ejecutar:

```bash
ros2 run g04_prii3_move_turtlebot draw_number
```

El TurtleBot realiza automáticamente una trayectoria con forma de:

```text
04
```

### Servicios

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

## Collision Avoidance

Ejecutar:

```bash
ros2 run g04_prii3_move_turtlebot collision_avoidance
```

El nodo utiliza el LiDAR mediante:

```text
/scan
```

El TurtleBot sigue realizando el número `04`.

Si detecta un obstáculo delante:

```text
TurtleBot → se detiene
```

Cuando el obstáculo desaparece:

```text
TurtleBot → continúa desde el punto donde se había detenido
```

---

# Sprint 2 - JetBot real

## Conexión al robot

El ordenador y el JetBot deben estar conectados a la misma red.

Se puede conectar mediante SSH:

```bash
ssh jetbot@IP_DEL_ROBOT
```

También se puede utilizar **VS Code Remote-SSH**.

El workspace del JetBot es:

```text
/home/jetbot/ros2_ws
```

## Preparación del JetBot

En cada terminal del JetBot:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/.bashrc
```

Comprobar el dominio:

```bash
echo $ROS_DOMAIN_ID
```

Debe aparecer:

```text
157
```

## Preparación del ordenador

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
source ~/.bashrc
```

## Draw Number

```bash
ros2 run g04_prii3_move_jetbot draw_number
```

El JetBot realiza automáticamente:

```text
04
```

### Servicios

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

Para repetir exactamente el recorrido se debe volver a colocar físicamente el robot en la posición inicial.

## Collision Avoidance

```bash
ros2 run g04_prii3_move_jetbot collision_avoidance
```

El nodo utiliza:

```text
/scan
```

Cuando detecta un obstáculo:

```text
JetBot → se detiene
```

Cuando desaparece:

```text
JetBot → continúa
```

---

# Sprint 3 - Navegación

En el Sprint 3 se trabaja con:

- Gazebo
- RViz
- Navigation2
- AMCL
- LiDAR
- Cámara
- OpenCV
- Marcadores ArUco

Paquete utilizado para la simulación:

```text
g04_prii3_nav_turtlebot
```

Actualmente se han realizado:

```text
PBI 3.2 - Navegación guiada mediante RViz
PBI 3.4 - Navegación autónoma
Detección de ArUcos
Selección de destino según el ID del ArUco
```

El apartado `predefined_navigation` todavía no está incluido.

---

# Sprint 3 - Preparación de la simulación

Entrar al workspace:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
source ~/.bashrc
```

Comprobar:

```bash
echo $ROS_DOMAIN_ID
```

Debe devolver:

```text
157
```

Seleccionar TurtleBot3 Waffle:

```bash
export TURTLEBOT3_MODEL=waffle
```

Añadir los modelos de Gazebo:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/g04_prii3_ws/src/f1l3_gazebo/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

---

# PBI 3.2 - Navegación guiada con RViz

Para este apartado se utiliza un launch independiente:

```text
pbi_3_2_rviz.launch.py
```

Ejecutar:

```bash
ros2 launch g04_prii3_nav_turtlebot pbi_3_2_rviz.launch.py
```

El launch inicia el entorno necesario para realizar la navegación guiada.

En RViz:

1. Seleccionar `2D Pose Estimate`.
2. Indicar la posición inicial del robot.
3. Indicar también su orientación.
4. Seleccionar `Nav2 Goal`.
5. Marcar una pose objetivo.
6. Nav2 calcula la ruta y mueve el TurtleBot hasta el destino.

La idea general es:

```text
RViz
  ↓
Pose inicial
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

AMCL se utiliza para estimar la posición del robot dentro de un mapa conocido.

Para ello intervienen principalmente:

```text
/map
/scan
/initialpose
/amcl_pose
```

La pose inicial se envía mediante:

```text
/initialpose
```

con mensajes:

```text
geometry_msgs/msg/PoseWithCovarianceStamped
```

AMCL publica la posición estimada mediante:

```text
/amcl_pose
```

también utilizando:

```text
geometry_msgs/msg/PoseWithCovarianceStamped
```

Conceptualmente:

```text
Mapa + LiDAR + odometría
          ↓
         AMCL
          ↓
Posición estimada del robot
```

AMCL se encarga de saber:

```text
¿Dónde está el robot dentro del mapa?
```

Navigation2 se encarga de:

```text
¿Cómo llegar hasta el destino?
```

---

# PBI 3.4 - Navegación autónoma

La navegación autónoma utiliza dos nodos propios:

```text
autonomous_navigation
aruco_destination
```

La secuencia general es:

```text
Pose inicial
     ↓
AMCL localiza el robot
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

El nodo:

```text
autonomous_navigation
```

coordina la navegación.

## Suscripciones

Está suscrito a:

```text
/amcl_pose
/destino_aruco
```

### /amcl_pose

Se utiliza para comprobar que AMCL ya está proporcionando una localización del robot.

Cuando llega un mensaje:

```text
self.localizado = True
```

### /destino_aruco

Recibe la pose final asociada al marcador detectado.

Tipo:

```text
geometry_msgs/msg/Pose2D
```

## Publicaciones

El nodo publica:

```text
/initialpose
```

para indicar a AMCL la posición inicial aproximada del robot.

## Navegación

Se utiliza un:

```text
ActionClient
```

con la acción:

```text
nav2_msgs/action/NavigateToPose
```

y el servidor:

```text
navigate_to_pose
```

El objetivo contiene:

```text
x
y
orientación
```

Navigation2 recibe el objetivo y se encarga de calcular y ejecutar la navegación.

---

# aruco_destination

El nodo:

```text
aruco_destination
```

se encarga de procesar las imágenes de la cámara y detectar los ArUcos.

## Suscripción

Está suscrito a:

```text
/camera/image_raw
```

Tipo de mensaje:

```text
sensor_msgs/msg/Image
```

La imagen ROS se convierte a OpenCV mediante:

```text
CvBridge
```

Después se convierte a escala de grises y se realiza la detección de ArUcos.

---

# Destinos ArUco

Actualmente se utilizan tres IDs:

```text
5
6
17
```

Cada ID tiene asociada una pose.

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

El ArUco solamente proporciona el ID.

Las coordenadas están asociadas al ID dentro del programa:

```text
DESTINOS[id_aruco]
```

---

# /destino_aruco

Cuando se detecta un marcador válido se publica:

```text
/destino_aruco
```

Tipo:

```text
geometry_msgs/msg/Pose2D
```

El mensaje contiene:

```text
x
y
theta
```

donde `theta` representa la orientación del robot.

La comunicación entre los nodos es:

```text
/camera/image_raw
        ↓
aruco_destination
        ↓
detección del ID
        ↓
DESTINOS[id]
        ↓
/destino_aruco
        ↓
autonomous_navigation
        ↓
NavigateToPose
        ↓
Nav2
```

---

# Ejecución de la navegación autónoma

Preparar la terminal:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
source ~/.bashrc
```

Seleccionar el modelo:

```bash
export TURTLEBOT3_MODEL=waffle
```

Añadir modelos:

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

## Tipos de mensajes

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

Acción utilizada para navegación:

```text
navigate_to_pose
nav2_msgs/action/NavigateToPose
```

---

# Sprint 3 - JetBot físico

Para trabajar con el JetBot físico se utiliza el workspace:

```text
/home/jetbot/ros2_ws
```

La comunicación entre el ordenador y el JetBot utiliza:

```text
ROS_DOMAIN_ID=157
```

El PC y el JetBot deben estar conectados a la misma red.

## Nodo base

En una terminal SSH:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/.bashrc

ros2 run jetbot_pro_ros2 jetbot
```

## LiDAR

En otra terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source ~/.bashrc

ros2 run rplidar_ros rplidar_composition --ros-args \
-p serial_port:=/dev/ttyACM1 \
-p serial_baudrate:=115200 \
-p frame_id:=laser_frame
```

El LiDAR publica:

```text
/scan
```

## Transformación del LiDAR

```bash
ros2 run tf2_ros static_transform_publisher \
0 0 0.15 3.14 0 0 \
base_link laser_frame
```

La cadena de transformaciones utilizada es:

```text
odom
 ↓
base_link
 ↓
laser_frame
```

## Mapa

Los archivos utilizados en el JetBot son:

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

Comprobar:

```bash
ros2 lifecycle get /map_server
```

Debe aparecer:

```text
active [3]
```

## AMCL físico

Ejecutar:

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

Comprobar:

```bash
ros2 lifecycle get /amcl
```

Debe aparecer:

```text
active [3]
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

## RViz desde el ordenador

En el PC:

```bash
source ~/.bashrc
source /opt/ros/humble/setup.bash

rviz2 -d ~/nav2.rviz
```

El mapa utilizado tiene:

```text
Resolución: 0.05 m/píxel
Tamaño: 546 x 540
```

Desde RViz se utiliza:

```text
2D Pose Estimate
```

para enviar la posición inicial mediante:

```text
/initialpose
```

---

# Estado actual del Sprint 3 físico

Actualmente se ha comprobado:

```text
Nodo base JetBot funcionando
LiDAR funcionando
/scan funcionando
TF odom -> base_link
TF base_link -> laser_frame
Mapa cargado
map_server activo
/map publicado
AMCL activo
RViz conectado al JetBot
/initialpose enviado desde RViz
```

El siguiente paso es terminar de comprobar la localización mediante:

```text
/amcl_pose
```

y la transformación:

```text
map -> base_link
```

antes de continuar con la navegación física.

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
│   │   ├── maps/
│   │   └── g04_prii3_nav_turtlebot/
│   │       ├── autonomous_navigation.py
│   │       └── aruco_destination.py
│   │
│   └── f1l3_gazebo/
│
├── .gitignore
└── README.md
```

Las carpetas generadas durante la compilación:

```text
build/
install/
log/
```

no deben almacenarse en el repositorio Git.
