import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class CollisionAvoidance(Node):

    # Constructor: configura el nodo.
    def __init__(self):
        super().__init__('collision_avoidance')

        # Crea el publisher que enviará movimientos por /cmd_vel.
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

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
            (0.30, 0.80, 7.85),

            # separación
            (0.30, 0.00, 2.50),

            # 4 abierto

            # subir izquierda
            (0.00, 0.80, 1.96),
            (0.30, 0.00, 1.67),

            # volver abajo
            (0.00, 0.80, 3.93),
            (0.30, 0.00, 1.67),

            # barra horizontal
            (0.00, 0.80, 1.96),
            (0.30, 0.00, 2.67),

            # subir derecha
            (0.00, 0.80, 1.96),
            (0.30, 0.00, 1.67),

            # bajar derecha y continuar
            (0.00, 0.80, 3.93),
            (0.30, 0.00, 3.33)
        ]

        # Índice del movimiento actual.
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

        # Selecciona las medidas de la parte frontal.
        # Parte frontal del TurtleBot
        frente = list(data.ranges[:20]) + list(data.ranges[-20:])

        # Empieza suponiendo que no hay obstáculo.
        self.obstaculo = False

        # Recorre todas las distancias frontales.
        for distancia in frente:

            # Si hay algo entre 0.12 y 0.30 m, marca obstáculo.
            if distancia > 0.12 and distancia < 0.30:
                self.obstaculo = True

    # Callback del timer: decide si parar o seguir dibujando.
    def timer_callback(self):

        # Si hay obstáculo, detiene el robot.
        # Si hay obstáculo, parar
        if self.obstaculo:
            self.parar()
            return

        # Si ya no quedan movimientos, termina el dibujo.
        # Si ya ha terminado el 04
        if self.movimiento >= len(self.movimientos):
            self.parar()
            return

        # Obtiene el movimiento actual.
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

    # Envía velocidad 0 para detener el robot.
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
        # Mantiene el nodo activo para ejecutar los callbacks.
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.parar()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
