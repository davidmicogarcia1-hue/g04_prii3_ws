import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger
from std_srvs.srv import Empty


class DrawNumber(Node):

    # Constructor: configura el nodo.
    def __init__(self):
        super().__init__('draw_number')

        # Crea el publisher que enviará movimientos por /cmd_vel.
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Crea los servicios y los conecta con sus callbacks.
        self.create_service(Trigger, '/detener_dibujo', self.detener)
        self.create_service(Trigger, '/reanudar_dibujo', self.reanudar)
        self.create_service(Trigger, '/reiniciar_dibujo', self.reiniciar)

        # Cliente para reiniciar el mundo de Gazebo.
        self.reset = self.create_client(Empty, '/reset_world')

        # velocidad lineal, velocidad angular, tiempo
        self.movimientos = [

            # 0
            (0.30, 0.80, 7.85),

            # Separación entre 0 y 4
            (0.30, 0.00, 2.50),

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

        # Índice del movimiento que se está ejecutando.
        self.movimiento = 0

        # Tiempo acumulado del movimiento actual.
        self.tiempo = 0.0

        # Estado de pausa del dibujo.
        self.pausado = False

        # Ejecuta timer_callback cada 0.05 segundos.
        self.timer = self.create_timer(0.05, self.timer_callback)

    # Callback del timer: controla la secuencia del dibujo.
    def timer_callback(self):

        # Si está pausado, no hace nada.
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

        # ESTA es la línea que publica el mensaje de movimiento.
        self.pub.publish(msg)

        # Suma el tiempo transcurrido.
        self.tiempo += 0.05

        # Si termina la duración del movimiento actual, pasa al siguiente.
        if self.tiempo >= duracion:
            self.parar()

            # Avanza al siguiente movimiento de la lista.
            self.movimiento += 1

            # Reinicia el tiempo para el siguiente movimiento.
            self.tiempo = 0.0

    # Envía velocidad 0 para detener el robot.
    def parar(self):

        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0

        # Publica el mensaje de parada.
        self.pub.publish(msg)

    # Callback del servicio que detiene el dibujo.
    def detener(self, request, response):

        # Activa la pausa.
        self.pausado = True

        # Detiene el robot.
        self.parar()

        response.success = True
        response.message = 'Dibujo detenido'

        return response

    # Callback del servicio que reanuda el dibujo.
    def reanudar(self, request, response):

        # Desactiva la pausa y continúa donde estaba.
        self.pausado = False

        response.success = True
        response.message = 'Dibujo reanudado'

        return response

    # Callback del servicio que reinicia el dibujo.
    def reiniciar(self, request, response):

        self.parar()

        # Vuelve al primer movimiento.
        self.movimiento = 0

        # Reinicia el tiempo.
        self.tiempo = 0.0

        # Quita la pausa.
        self.pausado = False

        # Llama al servicio /reset_world de Gazebo.
        self.reset.call_async(Empty.Request())

        response.success = True
        response.message = 'Dibujo reiniciado'

        return response


# Función principal: inicia ROS y mantiene el nodo funcionando.
def main(args=None):

    rclpy.init(args=args)

    # Crea el nodo y ejecuta su constructor.
    node = DrawNumber()

    try:
        # Mantiene el nodo activo para recibir callbacks.
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.parar()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
