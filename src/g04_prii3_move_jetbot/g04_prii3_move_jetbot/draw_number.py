import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger


class DrawNumber(Node):

    # Constructor: configura el nodo.
    def __init__(self):
        super().__init__('draw_number')

        # Crea el publisher que enviará movimientos por /cmd_vel.
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Crea el servicio para detener el dibujo.
        self.create_service(
            Trigger,
            '/detener_dibujo',
            self.detener
        )

        # Crea el servicio para reanudar el dibujo.
        self.create_service(
            Trigger,
            '/reanudar_dibujo',
            self.reanudar
        )

        # Crea el servicio para reiniciar el dibujo.
        self.create_service(
            Trigger,
            '/reiniciar_dibujo',
            self.reiniciar
        )

        # velocidad lineal, velocidad angular, tiempo

        self.movimientos = [
            # 0
            (0.10, 0.80, 7.85),

            # separación
            (0.10, 0.00, 4.50),

            # 4 abierto

            # subir izquierda
            (0.00, 0.80, 1.96),
            (0.10, 0.00, 2.50),

            # volver abajo
            (0.00, 0.80, 3.93),
            (0.10, 0.00, 2.50),

            # horizontal
            (0.00, 0.80, 1.96),
            (0.10, 0.00, 3.50),

            # subir derecha
            (0.00, 0.80, 1.96),
            (0.10, 0.00, 2.50),

            # bajar derecha
            (0.00, 0.80, 3.93),
            (0.10, 0.00, 5.00)
        ]

        # Índice del movimiento que se está ejecutando.
        self.movimiento = 0

        # Tiempo acumulado del movimiento actual.
        self.tiempo = 0.0

        # Indica si el dibujo está pausado.
        self.pausado = False

        # Ejecuta timer_callback cada 0.05 segundos.
        self.timer = self.create_timer(
            0.05,
            self.timer_callback
        )

    # Callback del timer: controla la secuencia del 04.
    def timer_callback(self):

        # Si está pausado, no continúa.
        if self.pausado:
            return

        # Si ya no quedan movimientos, detiene el robot.
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

    # Callback del servicio para detener.
    def detener(self, request, response):

        # Activa la pausa.
        self.pausado = True

        self.parar()

        response.success = True
        response.message = 'Dibujo detenido'

        return response

    # Callback del servicio para reanudar.
    def reanudar(self, request, response):

        # Quita la pausa y continúa donde estaba.
        self.pausado = False

        response.success = True
        response.message = 'Dibujo reanudado'

        return response

    # Callback del servicio para reiniciar.
    def reiniciar(self, request, response):

        self.parar()

        # Vuelve al primer movimiento.
        self.movimiento = 0

        # Reinicia el tiempo.
        self.tiempo = 0.0

        # Quita la pausa.
        self.pausado = False

        response.success = True
        response.message = 'Dibujo reiniciado'

        return response


# Función principal: inicia ROS y mantiene el nodo activo.
def main(args=None):

    rclpy.init(args=args)

    # Crea el nodo y ejecuta su constructor.
    node = DrawNumber()

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
