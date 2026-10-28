import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class CollisionAvoidance(Node):

    def __init__(self):
        super().__init__('collision_avoidance')

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

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

        self.movimiento = 0
        self.tiempo = 0.0

        self.obstaculo = False

        self.timer = self.create_timer(
            0.05,
            self.timer_callback
        )

    def laser_callback(self, data):

        # Parte frontal del TurtleBot
        frente = list(data.ranges[:20]) + list(data.ranges[-20:])

        self.obstaculo = False

        for distancia in frente:

            if distancia > 0.12 and distancia < 0.30:
                self.obstaculo = True

    def timer_callback(self):

        # Si hay obstáculo, parar
        if self.obstaculo:
            self.parar()
            return

        # Si ya ha terminado el 04
        if self.movimiento >= len(self.movimientos):
            self.parar()
            return

        lineal, angular, duracion = self.movimientos[self.movimiento]

        msg = Twist()

        msg.linear.x = lineal
        msg.angular.z = angular

        self.pub.publish(msg)

        self.tiempo += 0.05

        if self.tiempo >= duracion:

            self.parar()

            self.movimiento += 1
            self.tiempo = 0.0

    def parar(self):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        self.pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = CollisionAvoidance()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.parar()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()