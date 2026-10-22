# PRII3 - Grupo 04

Proyecto realizado para la asignatura **Proyecto RII 3: Robots Inteligentes**.

## Integrantes

* David Micó García
* Carlos Villar Cejalvo
* Marcos Anaya Benavente

---

# Requisitos generales

* Ubuntu 22.04
* ROS 2 Humble
* Python 3
* colcon

Para compilar todo el workspace:

```bash
cd ~/g04_prii3_ws
colcon build
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

El nodo principal es:

```text
dibujo04
```

## Ejecutar

Después de compilar y cargar el workspace:

```bash
ros2 launch g04_prii3_turtlesim dibujo04.launch.py
```

El programa inicia `turtlesim` y realiza automáticamente el dibujo del número `04`.

## Servicios

### Detener el dibujo

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

### Reanudar el dibujo

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

### Reiniciar el dibujo

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

---

# Sprint 2 - Movimiento y evitación de colisiones

En este Sprint se trabaja tanto con el **TurtleBot3 Waffle en simulación** como con el **JetBot real**.

Se han creado dos paquetes:

```text
g04_prii3_move_turtlebot
g04_prii3_move_jetbot
```

---

# Sprint 2 - TurtleBot3 en simulación

## Preparación

Seleccionar el modelo Waffle:

```bash
export TURTLEBOT3_MODEL=waffle
```

Abrir Gazebo:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

En otra terminal cargar el workspace:

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

## Collision Avoidance

Ejecutar:

```bash
ros2 run g04_prii3_move_turtlebot collision_avoidance
```

El nodo utiliza los datos del LiDAR publicados en:

```text
/scan
```

Si detecta un obstáculo delante del robot, detiene el movimiento.

Cuando el obstáculo desaparece, el TurtleBot continúa el recorrido.

---

# Sprint 2 - JetBot real

## Conexión al robot

El JetBot y el ordenador deben estar conectados a la misma red.

La conexión al robot puede realizarse mediante SSH:

```bash
ssh -X jetbot@IP_DEL_ROBOT
```

También se puede utilizar **VS Code Remote-SSH** para trabajar directamente sobre el workspace del JetBot.

El workspace del robot es:

```text
/home/jetbot/jetbot_ws
```

## Dominio ROS

Para evitar interferencias con otros robots se utiliza:

```bash
export ROS_DOMAIN_ID=4
```

Este valor debe establecerse tanto en el JetBot como en el ordenador.

## Iniciar el JetBot

En el robot:

```bash
export ROS_DOMAIN_ID=4
ros2 launch jetbot_pro_ros2 jetbot.py
```

Este launch inicia el control del robot, odometría y LiDAR.

---

## Draw Number

En el ordenador:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=4
```

Ejecutar:

```bash
ros2 run g04_prii3_move_jetbot draw_number
```

El JetBot realiza automáticamente el número:

```text
04
```

### Detener

```bash
ros2 service call /detener_dibujo std_srvs/srv/Trigger "{}"
```

### Reanudar

```bash
ros2 service call /reanudar_dibujo std_srvs/srv/Trigger "{}"
```

### Reiniciar

```bash
ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger "{}"
```

---

## Collision Avoidance

Ejecutar:

```bash
ros2 run g04_prii3_move_jetbot collision_avoidance
```

El nodo utiliza el LiDAR del JetBot mediante el topic:

```text
/scan
```

Cuando detecta un obstáculo delante del robot, el JetBot se detiene.

Cuando el obstáculo desaparece, el robot continúa automáticamente el recorrido del número `04`.

---

# Estructura principal del workspace

```text
g04_prii3_ws/
│
├── src/
│   ├── g04_prii3_turtlesim/
│   ├── g04_prii3_move_turtlebot/
│   └── g04_prii3_move_jetbot/
│
├── .gitignore
└── README.md
```

Las carpetas generadas por ROS 2:

```text
build/
install/
log/
```

no se incluyen en el repositorio.
