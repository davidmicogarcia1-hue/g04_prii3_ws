import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from nav2_msgs.action import NavigateToPose


class PredefinedNavigation(Node):

    def __init__(self):
        super().__init__('predefined_navigation')

        # Cliente de la acción de navegación de Nav2
        self.nav_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.goal_enviado = False

        # Esperamos un poco antes de mandar el destino
        self.timer = self.create_timer(2.0, self.enviar_destino)

    def enviar_destino(self):

        if self.goal_enviado:
            return

        if not self.nav_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Esperando a Navigation2...')
            return

        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()

        # --------------------------------------
        # DESTINO FIJO
        # CAMBIAREMOS ESTOS DOS VALORES
        # --------------------------------------
        goal.pose.pose.position.x = 0.0
        goal.pose.pose.position.y = 0.0
        goal.pose.pose.position.z = 0.0

        # Orientación final
        # z = 0 y w = 1 -> mirando en dirección 0 grados
        goal.pose.pose.orientation.x = 0.0
        goal.pose.pose.orientation.y = 0.0
        goal.pose.pose.orientation.z = 0.0
        goal.pose.pose.orientation.w = 1.0

        self.goal_enviado = True
        self.timer.cancel()

        self.get_logger().info(
            'Enviando destino: x=0.0, y=0.0'
        )

        future = self.nav_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Destino rechazado')
            return

        self.get_logger().info('Destino aceptado')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):

        distancia = feedback_msg.feedback.distance_remaining

        self.get_logger().info(
            f'Distancia restante: {distancia:.2f} m'
        )

    def result_callback(self, future):

        self.get_logger().info('Navegación terminada')


def main(args=None):

    rclpy.init(args=args)

    nodo = PredefinedNavigation()

    rclpy.spin(nodo)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
