import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class CollisionAvoidance(Node):

    # Constructor: configura el nodo.
    def __init__(self):
        super().__init__('collision_avoidance')

        # Crea el publisher que enviará movimientos por /cmd_vel.
        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Se suscribe al LiDAR; cada mensaje recibido ejecuta laser_callback.
        self.sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )

        # velocidad lineal, velocidad angular, tiempo
        self.movimientos = [
            # 0
            (0.10, 0.80, 7.85),

            # separación
            (0.10, 0.00, 4.50),

            # 4 abierto
            (0.00, 0.80, 1.96),
            (0.10, 0.00, 2.50),

            (0.00, 0.80, 3.93),
            (0.10, 0.00, 2.50),

            (0.00, 0.80, 1.96),
            (0.10, 0.00, 3.50),

            (0.00, 0.80, 1.96),
            (0.10, 0.00, 2.50),

            (0.00, 0.80, 3.93),
            (0.10, 0.00, 5.00)
        ]

        # Índice del movimiento que se está ejecutando.
        self.movimiento = 0

        # Tiempo acumulado del movimiento actual.
        self.tiempo = 0.0

        # Indica si el LiDAR detecta un obstáculo.
        self.obstaculo = False

        # Ejecuta timer_callback cada 0.05 segundos.
        self.timer = self.create_timer(
            0.05,
            self.timer_callback
        )

    # Callback del LiDAR: comprueba si hay obstáculos delante.
    def laser_callback(self, data):

        # Parte FRONTAL del JetBot.
        # En nuestro LiDAR el frente está en los extremos
        # de la lista ranges.
        frente = list(data.ranges[:20]) + list(data.ranges[-20:])

        # Empieza suponiendo que no hay obstáculo.
        self.obstaculo = False

        # Recorre las distancias de la zona frontal.
        for distancia in frente:

            # Si detecta algo válido a menos de 0.30 m, marca obstáculo.
            if distancia >= data.range_min and distancia < 0.30:
                self.obstaculo = True

    # Callback del timer: decide si parar o seguir dibujando.
    def timer_callback(self):

        # Si hay obstáculo, detiene el robot.
        if self.obstaculo:
            self.parar()
            return

        # Si ya no quedan movimientos, termina el dibujo.
        if self.movimiento >= len(self.movimientos):
            self.parar()
            return

        # Obtiene el movimiento actual de la lista.
        lineal, angular, duracion = self.movimientos[self.movimiento]

        msg = Twist()

        msg.linear.x = lineal
        msg.angular.z = angular

        # ESTA es la línea que publica el movimiento.
        self.pub.publish(msg)

        # Suma el tiempo transcurrido.
        self.tiempo += 0.05

        # Si termina este movimiento, pasa al siguiente.
        if self.tiempo >= duracion:

            self.parar()

            # Avanza al siguiente movimiento.
            self.movimiento += 1

            # Reinicia el tiempo del nuevo movimiento.
            self.tiempo = 0.0

    # Detiene el robot enviando velocidad 0.
    def parar(self):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        # Publica el mensaje de parada.
        self.pub.publish(msg)


# Función principal: inicia ROS y mantiene el nodo activo.
def main(args=None):

    rclpy.init(args=args)

    # Crea el nodo y ejecuta su constructor.
    node = CollisionAvoidance()

    try:
        # Mantiene el nodo activo para ejecutar callbacks.
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.parar()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
