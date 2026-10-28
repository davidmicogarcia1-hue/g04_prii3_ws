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

---

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

### Prueba con un obstáculo en Gazebo

Se puede utilizar un cubo de Gazebo como obstáculo.

Ejemplo de fichero `cubo.sdf`:

```xml
<sdf version="1.6">
  <model name="cubo">
    <static>false</static>

    <link name="link">

      <collision name="collision">
        <geometry>
          <box>
            <size>0.5 0.5 0.5</size>
          </box>
        </geometry>
      </collision>

      <visual name="visual">
        <geometry>
          <box>
            <size>0.5 0.5 0.5</size>
          </box>
        </geometry>
      </visual>

    </link>
  </model>
</sdf>
```

Para añadir el cubo:

```bash
ros2 service call /spawn_entity gazebo_msgs/srv/SpawnEntity "{name: 'cubo', xml: '$(cat ~/cubo.sdf)', robot_namespace: '', initial_pose: {position: {x: 0.5, y: 0.0, z: 1.0}}, reference_frame: 'world'}"
```

El cubo aparece en el aire y cae delante del robot.

Para esperar tres segundos:

```bash
sleep 3
```

Para eliminarlo:

```bash
ros2 service call /delete_entity gazebo_msgs/srv/DeleteEntity "{name: 'cubo'}"
```

La prueba esperada es:

```text
TurtleBot realiza el 04
        ↓
aparece y cae el cubo
        ↓
el LiDAR detecta el obstáculo
        ↓
TurtleBot se detiene
        ↓
desaparece el cubo
        ↓
TurtleBot continúa el 04
```

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
/home/jetbot/jetbot_ws
```

---

## Dominio ROS

Para evitar interferencias con otros robots utilizamos:

```bash
export ROS_DOMAIN_ID=4
```

Debe establecerse tanto en el JetBot como en el ordenador.

---

## Iniciar el JetBot

En una terminal del JetBot:

```bash
export ROS_DOMAIN_ID=4
ros2 launch jetbot_pro_ros2 jetbot.py
```

Esta terminal debe permanecer ejecutándose.

El launch inicia el control del robot, la odometría y el LiDAR.

---

## Preparar el PC

En otra terminal del ordenador:

```bash
cd ~/g04_prii3_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=4
```

---

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

---

## Collision Avoidance

```bash
ros2 run g04_prii3_move_jetbot collision_avoidance
```

El nodo utiliza el LiDAR mediante:

```text
/scan
```

El JetBot dibuja el número `04`.

Cuando detecta un obstáculo delante:

```text
JetBot → se detiene
```

Cuando el obstáculo desaparece:

```text
JetBot → continúa el recorrido
```

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

Las carpetas generadas durante la compilación:

```text
build/
install/
log/
```

no se incluyen en el repositorio Git.