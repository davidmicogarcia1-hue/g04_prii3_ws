import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger
from std_srvs.srv import Empty


class DrawNumber(Node):

    def __init__(self):
        super().__init__('draw_number')

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_service(Trigger, '/detener_dibujo', self.detener)
        self.create_service(Trigger, '/reanudar_dibujo', self.reanudar)
        self.create_service(Trigger, '/reiniciar_dibujo', self.reiniciar)

        self.reset = self.create_client(Empty, '/reset_world')

        # velocidad lineal, velocidad angular, tiempo
        self.movimientos = [

            # 0
            (0.30, 0.80, 7.85),

            # Separación entre 0 y 4
            (0.30, 0.00, 2.50),

            # =====================
            #       4 ABIERTO
            #
            #   |       |
            #   |_______|
            #           |
            #           |
            # =====================

            # Girar 90º izquierda
            (0.00, 0.80, 1.96),

            # Subir izquierda 0.50 m aprox.
            (0.30, 0.00, 1.67),

            # Media vuelta
            (0.00, 0.80, 3.93),

            # Volver al cruce
            (0.30, 0.00, 1.67),

            # Girar hacia la derecha del dibujo
            (0.00, 0.80, 1.96),

            # Barra horizontal 0.80 m aprox.
            (0.30, 0.00, 2.67),

            # Girar hacia arriba
            (0.00, 0.80, 1.96),

            # Subir pata derecha
            (0.30, 0.00, 1.67),

            # Media vuelta
            (0.00, 0.80, 3.93),

            # Bajar y prolongar la pata derecha
            (0.30, 0.00, 3.33)
        ]

        self.movimiento = 0
        self.tiempo = 0.0
        self.pausado = False

        self.timer = self.create_timer(0.05, self.timer_callback)

    def timer_callback(self):

        if self.pausado:
            return

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

    def detener(self, request, response):

        self.pausado = True
        self.parar()

        response.success = True
        response.message = 'Dibujo detenido'

        return response

    def reanudar(self, request, response):

        self.pausado = False

        response.success = True
        response.message = 'Dibujo reanudado'

        return response

    def reiniciar(self, request, response):

        self.parar()

        self.movimiento = 0
        self.tiempo = 0.0
        self.pausado = False

        self.reset.call_async(Empty.Request())

        response.success = True
        response.message = 'Dibujo reiniciado'

        return response


def main(args=None):

    rclpy.init(args=args)

    node = DrawNumber()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.parar()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()