import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, Empty


class DrawNumber(Node):

    def __init__(self):
        super().__init__('draw_number')

        # Publicador para mover el TurtleBot
        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Servicio de Gazebo para devolver el robot
        # a su posición inicial
        self.reset_client = self.create_client(
            Empty,
            '/reset_world'
        )

        # Servicios de nuestro nodo
        self.create_service(
            Trigger,
            'detener_dibujo',
            self.detener
        )

        self.create_service(
            Trigger,
            'reanudar_dibujo',
            self.reanudar
        )

        self.create_service(
            Trigger,
            'reiniciar_dibujo',
            self.reiniciar
        )

        self.pausado = False
        self.paso = 0
        self.tiempo = 0.0
        self.reset_future = None

        # Cada acción:
        # ('move', velocidad_lineal, velocidad_angular, tiempo)

        self.acciones = [

            # ======================
            # NUMERO 0
            # ======================

            # Círculo completo
            ('move', 0.30, 0.80, 7.85),

            # ======================
            # IR HACIA EL 4
            # ======================

            ('move', 0.30, 0.00, 4.00),

            # ======================
            # NUMERO 4
            # ======================

            # Girar 45 grados
            ('move', 0.00, 0.80, 0.98),

            # Diagonal
            ('move', 0.30, 0.00, 2.67),

            # Girar -135 grados
            ('move', 0.00, -0.80, 2.95),

            # Palo vertical
            ('move', 0.30, 0.00, 4.00),

            # Girar 180 grados
            ('move', 0.00, 0.80, 3.93),

            # Subir hasta la mitad
            ('move', 0.30, 0.00, 2.00),

            # Girar 90 grados
            ('move', 0.00, 0.80, 1.96),

            # Barra horizontal
            ('move', 0.30, 0.00, 2.67),
        ]

        # Ejecutar control cada 0.05 segundos
        self.timer = self.create_timer(
            0.05,
            self.control
        )


    def control(self):

        # Esperar mientras Gazebo se reinicia
        if self.reset_future is not None:

            if not self.reset_future.done():
                return

            self.reset_future = None

        # Si está pausado, no mover
        if self.pausado:
            return

        # Si hemos terminado
        if self.paso >= len(self.acciones):

            self.parar()
            return

        accion = self.acciones[self.paso]

        velocidad_lineal = accion[1]
        velocidad_angular = accion[2]
        duracion = accion[3]

        msg = Twist()

        msg.linear.x = velocidad_lineal
        msg.angular.z = velocidad_angular

        self.pub.publish(msg)

        self.tiempo += 0.05

        # Pasar a la siguiente acción
        if self.tiempo >= duracion:

            self.parar()

            self.tiempo = 0.0
            self.paso += 1


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

        self.pausado = False
        self.paso = 0
        self.tiempo = 0.0

        # Devolver robot a posición inicial
        self.reset_future = self.reset_client.call_async(
            Empty.Request()
        )

        response.success = True
        response.message = 'Dibujo reiniciado'

        return response


    def parar(self):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        self.pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    nodo = DrawNumber()

    try:
        rclpy.spin(nodo)

    except KeyboardInterrupt:
        pass

    finally:

        if rclpy.ok():
            nodo.parar()

        nodo.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
