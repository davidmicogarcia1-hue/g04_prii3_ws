import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, Empty
from turtlesim.srv import SetPen


class Dibujo04(Node):

    def __init__(self):
        super().__init__('dibujo04')

        # Publicador para mover la tortuga
        self.pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Clientes para servicios de turtlesim
        self.pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        self.reset_client = self.create_client(
            Empty,
            '/reset'
        )

        # Esperamos a que los servicios estén disponibles
        self.pen_client.wait_for_service()
        self.reset_client.wait_for_service()

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

        # Variables de control
        self.pausado = False
        self.paso = 0
        self.tiempo = 0.0

        self.future = None
        self.reset_future = None

        # --------------------------------
        # SECUENCIA PARA DIBUJAR EL "04"
        # --------------------------------

        self.acciones = [

            # ============================
            # COLOCARSE PARA DIBUJAR EL 0
            # ============================

            ('pen_off',),

            # Girar 180 grados
            ('move', 0.0, 1.0, 3.14),

            # Ir hacia la izquierda
            ('move', 1.0, 0.0, 2.3),

            # ============================
            # DIBUJAR EL 0
            # ============================

            ('pen_on',),

            # Avanzar y girar a la vez
            # Hace un círculo completo
            ('move', 1.0, 1.0, 6.28),

            # ============================
            # IR HACIA EL 4
            # ============================

            ('pen_off',),

            # Girar 180 grados
            ('move', 0.0, 1.0, 3.14),

            # Ir hacia la derecha
            ('move', 1.0, 0.0, 3.0),

            # ============================
            # DIAGONAL DEL 4
            # ============================

            # Girar 45 grados
            ('move', 0.0, 1.0, 0.79),

            ('pen_on',),

            # Dibujar diagonal
            ('move', 1.0, 0.0, 2.8),

            # ============================
            # PALO VERTICAL DEL 4
            # ============================

            # Girar -135 grados
            ('move', 0.0, -1.0, 2.36),

            # Dibujar hacia abajo
            ('move', 1.0, 0.0, 4.0),

            # ============================
            # COLOCARSE PARA LA BARRA
            # ============================

            ('pen_off',),

            # Mirar hacia arriba
            ('move', 0.0, 1.0, 3.14),

            # Subir
            ('move', 1.0, 0.0, 2.0),

            # Girar hacia la izquierda
            ('move', 0.0, 1.0, 1.57),

            # Ir a la izquierda
            ('move', 1.0, 0.0, 2.0),

            # Girar hacia la derecha
            ('move', 0.0, 1.0, 3.14),

            # ============================
            # BARRA HORIZONTAL DEL 4
            # ============================

            ('pen_on',),

            # Dibujar barra horizontal
            ('move', 1.0, 0.0, 3.0),
        ]

        # Ejecutamos control cada 0.01 segundos
        self.timer = self.create_timer(
            0.01,
            self.control
        )


    def control(self):

        # Si estamos esperando al reset
        if self.reset_future is not None:

            if not self.reset_future.done():
                return

            self.reset_future = None

        # Si el dibujo está pausado
        if self.pausado:
            return

        # Si estamos esperando a un servicio del lápiz
        if self.future is not None:

            if not self.future.done():
                return

            self.future = None
            self.paso += 1
            return

        # Si hemos terminado todas las acciones
        if self.paso >= len(self.acciones):

            self.parar()
            return

        accion = self.acciones[self.paso]

        tipo = accion[0]

        # -------------------------
        # APAGAR EL LÁPIZ
        # -------------------------

        if tipo == 'pen_off':

            req = SetPen.Request()

            req.off = 1

            self.future = self.pen_client.call_async(req)


        # -------------------------
        # ENCENDER EL LÁPIZ
        # -------------------------

        elif tipo == 'pen_on':

            req = SetPen.Request()

            req.r = 255
            req.g = 255
            req.b = 255
            req.width = 3
            req.off = 0

            self.future = self.pen_client.call_async(req)


        # -------------------------
        # MOVER CON TWIST
        # -------------------------

        elif tipo == 'move':

            velocidad_lineal = accion[1]
            velocidad_angular = accion[2]
            duracion = accion[3]

            msg = Twist()

            msg.linear.x = velocidad_lineal
            msg.angular.z = velocidad_angular

            self.pub.publish(msg)

            self.tiempo += 0.01

            # Cuando termina el tiempo de la acción
            if self.tiempo >= duracion:

                self.parar()

                self.tiempo = 0.0
                self.paso += 1


    # =============================
    # SERVICIO DETENER
    # =============================

    def detener(self, request, response):

        self.pausado = True

        self.parar()

        response.success = True
        response.message = 'Dibujo detenido'

        return response


    # =============================
    # SERVICIO REANUDAR
    # =============================

    def reanudar(self, request, response):

        self.pausado = False

        response.success = True
        response.message = 'Dibujo reanudado'

        return response


    # =============================
    # SERVICIO REINICIAR
    # =============================

    def reiniciar(self, request, response):

        self.parar()

        self.pausado = False
        self.paso = 0
        self.tiempo = 0.0
        self.future = None

        # Reinicia turtlesim y borra el dibujo
        self.reset_future = self.reset_client.call_async(
            Empty.Request()
        )

        response.success = True
        response.message = 'Dibujo reiniciado'

        return response


    # =============================
    # PARAR LA TORTUGA
    # =============================

    def parar(self):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        self.pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    nodo = Dibujo04()

    try:
        rclpy.spin(nodo)

    except KeyboardInterrupt:
        pass

    nodo.parar()

    nodo.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
