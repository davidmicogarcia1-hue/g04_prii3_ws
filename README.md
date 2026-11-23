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
- TurtleBot3
- Navigation2

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

Cada vez que se abra una terminal nueva se debe volver a cargar el workspace:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

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

- **JetBot real**
- **TurtleBot3 Waffle en simulación**

Los paquetes utilizados son:

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

Seleccionar el modelo Waffle:

```bash
export TURTLEBOT3_MODEL=waffle
```

Abrir Gazebo con un mundo vacío:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

En otra terminal:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

## Draw Number

Ejecutar:

```bash
ros2 run g04_prii3_move_turtlebot draw_number
```

El TurtleBot realiza automáticamente una trayectoria que representa el número:

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

---

## Collision Avoidance

Ejecutar:

```bash
ros2 run g04_prii3_move_turtlebot collision_avoidance
```

El nodo utiliza el LiDAR del TurtleBot mediante:

```text
/scan
```

El robot continúa realizando el número `04`.

Si el LiDAR detecta un obstáculo delante del robot, el TurtleBot se detiene.

Cuando el obstáculo desaparece, continúa automáticamente el recorrido desde el punto en el que se había detenido.

---

# Sprint 2 - JetBot real

## Conexión al robot

El ordenador y el JetBot deben encontrarse en la misma red.

Conexión mediante SSH:

```bash
ssh -X jetbot@IP_DEL_ROBOT
```

También se puede utilizar **VS Code Remote-SSH**.

El workspace instalado en el JetBot es:

```text
/home/jetbot/ros2_ws
```

## Dominio ROS

El ordenador y el JetBot deben utilizar el mismo `ROS_DOMAIN_ID`.

Ejemplo:

```bash
export ROS_DOMAIN_ID=157
```

Debe configurarse tanto en el JetBot como en el ordenador.

## Draw Number

```bash
ros2 run g04_prii3_move_jetbot draw_number
```

El JetBot realiza automáticamente el número:

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

En el robot real, reiniciar el nodo reinicia la secuencia del dibujo. Para repetir exactamente el recorrido desde la misma posición se debe volver a colocar físicamente el robot en el punto inicial.

## Collision Avoidance

```bash
ros2 run g04_prii3_move_jetbot collision_avoidance
```

El nodo utiliza el LiDAR mediante:

```text
/scan
```

Cuando detecta un obstáculo delante:

```text
JetBot → se detiene
```

Cuando el obstáculo desaparece:

```text
JetBot → continúa el recorrido
```

---

# Sprint 3 - Navegación

En este Sprint se trabaja con navegación mediante:

- Gazebo
- RViz
- Navigation2
- AMCL
- LiDAR
- Cámara
- OpenCV
- Marcadores ArUco

Para la simulación se utiliza el paquete:

```text
g04_prii3_nav_turtlebot
```

Actualmente se han implementado:

```text
Navegación guiada mediante RViz
Navegación autónoma
Detección de ArUcos
Selección de destino según el ID del ArUco
```

---

# Sprint 3 - TurtleBot3 en simulación

## Preparación

Entrar al workspace:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Seleccionar TurtleBot3 Waffle:

```bash
export TURTLEBOT3_MODEL=waffle
```

Configurar el dominio utilizado en simulación:

```bash
export ROS_DOMAIN_ID=44
```

Añadir los modelos de Gazebo:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/g04_prii3_ws/src/f1l3_gazebo/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

---

# PBI 3.2 - Navegación guiada mediante RViz

Para este apartado se utiliza Gazebo, Nav2 y RViz.

Se dispone de un launch independiente:

```text
pbi_3_2_rviz.launch.py
```

Ejecutar:

```bash
ros2 launch g04_prii3_nav_turtlebot pbi_3_2_rviz.launch.py
```

El launch inicia:

```text
Gazebo
Nav2
RViz
Mapa de F1L3
```

Una vez abierto RViz:

1. Seleccionar `2D Pose Estimate`.
2. Indicar la posición y orientación inicial del TurtleBot.
3. Seleccionar `Nav2 Goal`.
4. Indicar una pose objetivo.
5. Nav2 calcula la trayectoria y navega hasta el destino.

La navegación utiliza:

```text
/map
/scan
/initialpose
/amcl_pose
/cmd_vel
```

AMCL se encarga de estimar la posición del robot dentro del mapa.

Nav2 se encarga de calcular y ejecutar la navegación hasta la pose seleccionada.

---

# PBI 3.4 - Navegación autónoma

La navegación autónoma utiliza dos nodos propios:

```text
autonomous_navigation
aruco_destination
```

## autonomous_navigation

El nodo:

```text
autonomous_navigation
```

realiza la secuencia principal de navegación.

Está suscrito a:

```text
/amcl_pose
/destino_aruco
```

Publica la pose inicial mediante:

```text
/initialpose
```

Y utiliza la acción:

```text
navigate_to_pose
```

de Navigation2.

La secuencia es:

```text
Publicar pose inicial
        ↓
AMCL localiza el robot
        ↓
Navegar hasta la puerta
        ↓
Esperar detección de ArUco
        ↓
Recibir destino
        ↓
Navegar hasta la pose final
```

---

## aruco_destination

El nodo:

```text
aruco_destination
```

está suscrito a:

```text
/camera/image_raw
```

Las imágenes se convierten a OpenCV mediante `CvBridge`.

Después se realiza la detección de marcadores ArUco.

Cuando se detecta un marcador conocido, se obtiene su ID y se busca su pose asociada.

Los IDs utilizados actualmente son:

```text
5
6
17
```

Cada marcador tiene asociada una pose diferente del mapa.

El nodo publica el destino mediante:

```text
/destino_aruco
```

utilizando:

```text
geometry_msgs/msg/Pose2D
```

El mensaje contiene:

```text
x
y
theta
```

---

# Destinos ArUco

Los destinos utilizados actualmente son:

```text
ID 5
x = -3.3882
y = 1.8334
gamma = 2.8143
```

```text
ID 6
x = -3.2034
y = 7.6416
gamma = -2.5406
```

```text
ID 17
x = 2.169
y = 8.444
gamma = 1.332
```

El ID del ArUco no contiene directamente estas coordenadas.

El programa detecta el ID y consulta las coordenadas asociadas en el diccionario `DESTINOS`.

---

# Comunicación entre nodos

La comunicación principal del sistema es:

```text
/camera/image_raw
        ↓
aruco_destination
        ↓
/destino_aruco
        ↓
autonomous_navigation
        ↓
NavigateToPose
        ↓
Nav2
        ↓
/cmd_vel
        ↓
TurtleBot3
```

AMCL interviene en la localización:

```text
/initialpose
        ↓
AMCL
        ↓
/amcl_pose
```

El LiDAR proporciona las medidas mediante:

```text
/scan
```

---

# Ejecución de la navegación autónoma

Antes de ejecutar, cargar el workspace:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Configurar:

```bash
export TURTLEBOT3_MODEL=waffle
export ROS_DOMAIN_ID=44
```

Añadir los modelos:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/g04_prii3_ws/src/f1l3_gazebo/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

Ejecutar la demo autónoma:

```bash
ros2 launch g04_prii3_nav_turtlebot autonomous_demo.launch.py
```

Durante la ejecución se inicia el entorno de simulación y el robot realiza la secuencia automática.

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

Tipos de mensajes principales:

```text
/scan
sensor_msgs/msg/LaserScan

/initialpose
geometry_msgs/msg/PoseWithCovarianceStamped

/amcl_pose
geometry_msgs/msg/PoseWithCovarianceStamped

/camera/image_raw
sensor_msgs/msg/Image

/destino_aruco
geometry_msgs/msg/Pose2D

/cmd_vel
geometry_msgs/msg/Twist
```

La navegación utiliza además la acción:

```text
navigate_to_pose
nav2_msgs/action/NavigateToPose
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
