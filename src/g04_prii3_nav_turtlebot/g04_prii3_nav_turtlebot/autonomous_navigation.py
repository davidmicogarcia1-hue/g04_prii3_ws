import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import PoseWithCovarianceStamped

from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus


# ---------------------------------------------------------
# POSE INICIAL
# ---------------------------------------------------------

INICIO_X = -0.6283862590789795
INICIO_Y = -5.823587417602539
INICIO_GAMMA = -0.014495306414798126


# ---------------------------------------------------------
# POSE DELANTE DE LA PUERTA
# ---------------------------------------------------------

PUERTA_X = 1.4158906566341665
PUERTA_Y = -4.347381311390621
PUERTA_GAMMA = 1.6900862527143428


class AutonomousNavigation(Node):

    def __init__(self):

        super().__init__('autonomous_navigation')

        # Publisher para indicar a AMCL
        # dónde empieza el robot
        self.initial_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

        # Subscriber para saber cuándo AMCL
        # ya ha aceptado la pose inicial
        self.amcl_pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.amcl_pose_callback,
            10
        )

        # Recibe el destino correspondiente
        # al ArUco detectado
        self.destino_sub = self.create_subscription(
            Pose2D,
            '/destino_aruco',
            self.destino_callback,
            10
        )

        # Cliente de Navigation2
        self.nav_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Variables de control
        self.localizado = False

        self.puerta_objetivo_enviado = False
        self.puerta_alcanzada = False

        self.destino_enviado = False

        # Repetimos la pose inicial cada segundo
        # hasta que AMCL confirme la localización
        self.timer_pose = self.create_timer(
            1.0,
            self.comprobar_localizacion
        )

        # Cuando AMCL esté preparado,
        # intenta ir a la puerta
        self.timer_puerta = self.create_timer(
            1.0,
            self.intentar_ir_a_puerta
        )

        self.get_logger().info(
            'Navegación autónoma iniciada'
        )


    # -----------------------------------------------------
    # PASO 1
    # PUBLICAR POSE INICIAL HASTA QUE AMCL LA ACEPTE
    # -----------------------------------------------------

    def comprobar_localizacion(self):

        if self.localizado:
            return

        self.publicar_pose_inicial()


    def publicar_pose_inicial(self):

        msg = PoseWithCovarianceStamped()

        msg.header.frame_id = 'map'
        msg.header.stamp = \
            self.get_clock().now().to_msg()

        msg.pose.pose.position.x = INICIO_X
        msg.pose.pose.position.y = INICIO_Y

        # Gamma -> quaternion
        msg.pose.pose.orientation.z = \
            math.sin(INICIO_GAMMA / 2.0)

        msg.pose.pose.orientation.w = \
            math.cos(INICIO_GAMMA / 2.0)

        # Incertidumbre inicial
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.0685

        self.initial_pose_pub.publish(msg)

        self.get_logger().info(
            'Publicando pose inicial...'
        )


    def amcl_pose_callback(self, msg):

        if self.localizado:
            return

        self.localizado = True

        # Ya no hace falta seguir publicando
        self.timer_pose.cancel()

        self.get_logger().info(
            'AMCL ha aceptado la pose inicial'
        )


    # -----------------------------------------------------
    # PASO 2
    # IR HASTA LA PUERTA
    # -----------------------------------------------------

    def intentar_ir_a_puerta(self):

        # Primero necesitamos localización
        if not self.localizado:
            return

        # Evitamos mandar el mismo objetivo
        if self.puerta_objetivo_enviado:
            return

        if self.puerta_alcanzada:
            return

        # Nav2 todavía puede estar arrancando
        if not self.nav_client.server_is_ready():
            return

        self.puerta_objetivo_enviado = True

        self.get_logger().info(
            'Navegando hacia la puerta...'
        )

        self.enviar_objetivo(
            PUERTA_X,
            PUERTA_Y,
            PUERTA_GAMMA,
            'puerta'
        )


    # -----------------------------------------------------
    # PASO 3
    # RECIBIR DESTINO DEL ARUCO
    # -----------------------------------------------------

    def destino_callback(self, msg):

        # Solo leemos el destino después
        # de llegar a la puerta
        if not self.puerta_alcanzada:
            return

        if self.destino_enviado:
            return

        if not self.nav_client.server_is_ready():
            return

        self.destino_enviado = True

        self.get_logger().info(
            'Destino recibido desde el ArUco'
        )

        self.get_logger().info(
            f'x={msg.x:.2f}, '
            f'y={msg.y:.2f}, '
            f'gamma={msg.theta:.2f}'
        )

        self.enviar_objetivo(
            msg.x,
            msg.y,
            msg.theta,
            'final'
        )


    # -----------------------------------------------------
    # ENVIAR OBJETIVO A NAV2
    # -----------------------------------------------------

    def enviar_objetivo(
        self,
        x,
        y,
        gamma,
        tipo
    ):

        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = \
            self.get_clock().now().to_msg()

        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y

        goal.pose.pose.orientation.z = \
            math.sin(gamma / 2.0)

        goal.pose.pose.orientation.w = \
            math.cos(gamma / 2.0)

        future = self.nav_client.send_goal_async(
            goal
        )

        future.add_done_callback(
            lambda f:
            self.goal_response_callback(
                f,
                tipo
            )
        )


    # -----------------------------------------------------
    # NAV2 ACEPTA O RECHAZA EL OBJETIVO
    # -----------------------------------------------------

    def goal_response_callback(
        self,
        future,
        tipo
    ):

        goal_handle = future.result()

        if not goal_handle.accepted:

            self.get_logger().info(
                'Objetivo rechazado. '
                'Se volverá a intentar.'
            )

            # Si Nav2 todavía estaba arrancando,
            # permitimos volver a intentarlo
            if tipo == 'puerta':
                self.puerta_objetivo_enviado = False

            elif tipo == 'final':
                self.destino_enviado = False

            return

        self.get_logger().info(
            'Objetivo aceptado'
        )

        result_future = \
            goal_handle.get_result_async()

        result_future.add_done_callback(
            lambda f:
            self.result_callback(
                f,
                tipo
            )
        )


    # -----------------------------------------------------
    # RESULTADO DE LA NAVEGACIÓN
    # -----------------------------------------------------

    def result_callback(
        self,
        future,
        tipo
    ):

        resultado = future.result()

        if resultado.status != \
                GoalStatus.STATUS_SUCCEEDED:

            self.get_logger().info(
                'No se pudo alcanzar el objetivo'
            )

            if tipo == 'puerta':
                self.puerta_objetivo_enviado = False

            elif tipo == 'final':
                self.destino_enviado = False

            return

        if tipo == 'puerta':

            self.puerta_alcanzada = True

            self.get_logger().info(
                'Puerta alcanzada'
            )

            self.get_logger().info(
                'Esperando ArUco...'
            )

        elif tipo == 'final':

            self.get_logger().info(
                'DESTINO FINAL ALCANZADO'
            )


def main(args=None):

    rclpy.init(args=args)

    node = AutonomousNavigation()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
