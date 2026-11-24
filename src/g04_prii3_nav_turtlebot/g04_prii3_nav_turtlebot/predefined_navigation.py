import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus


INICIO_X = -0.6283862590789795
INICIO_Y = -5.823587417602539
INICIO_GAMMA = -0.014495306414798126

FINAL_X = 2.169
FINAL_Y = 8.444
FINAL_GAMMA = 1.332


class PredefinedNavigation(Node):
    def __init__(self):
        super().__init__('predefined_navigation')

        self.initial_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

        self.amcl_pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.amcl_pose_callback,
            10
        )

        self.nav_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.localizado = False
        self.objetivo_enviado = False

        self.timer_pose = self.create_timer(
            1.0,
            self.publicar_pose_inicial
        )

        self.timer_nav = self.create_timer(
            1.0,
            self.intentar_navegar
        )

        self.get_logger().info('Navegacion predefinida iniciada')

    def publicar_pose_inicial(self):
        if self.localizado:
            return

        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.pose.pose.position.x = INICIO_X
        msg.pose.pose.position.y = INICIO_Y

        msg.pose.pose.orientation.z = math.sin(INICIO_GAMMA / 2.0)
        msg.pose.pose.orientation.w = math.cos(INICIO_GAMMA / 2.0)

        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.0685

        self.initial_pose_pub.publish(msg)
        self.get_logger().info('Publicando pose inicial predefinida')

    def amcl_pose_callback(self, msg):
        if self.localizado:
            return

        self.localizado = True
        self.timer_pose.cancel()
        self.get_logger().info('Robot localizado por AMCL')

    def intentar_navegar(self):
        if not self.localizado:
            return

        if self.objetivo_enviado:
            return

        if not self.nav_client.server_is_ready():
            return

        self.objetivo_enviado = True
        self.enviar_objetivo()

    def enviar_objetivo(self):
        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()

        goal.pose.pose.position.x = FINAL_X
        goal.pose.pose.position.y = FINAL_Y

        goal.pose.pose.orientation.z = math.sin(FINAL_GAMMA / 2.0)
        goal.pose.pose.orientation.w = math.cos(FINAL_GAMMA / 2.0)

        self.get_logger().info(
            f'Enviando destino final: x={FINAL_X:.3f}, '
            f'y={FINAL_Y:.3f}, gamma={FINAL_GAMMA:.3f}'
        )

        future = self.nav_client.send_goal_async(goal)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Objetivo rechazado')
            self.objetivo_enviado = False
            return

        self.get_logger().info('Objetivo aceptado')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        resultado = future.result()

        if resultado.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('DESTINO PREDEFINIDO ALCANZADO')
        else:
            self.get_logger().info('No se pudo alcanzar el destino')
            self.objetivo_enviado = False


def main(args=None):
    rclpy.init(args=args)
    node = PredefinedNavigation()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
