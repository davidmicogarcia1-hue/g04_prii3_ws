import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose2D

from cv_bridge import CvBridge

import cv2


DESTINOS = {

    5: (
        -3.3882179278364295,
        1.833430544730172,
        2.8143108387285256
    ),

    6: (
        -3.2033594467599604,
        7.641596806469504,
        -2.54057856469949
    ),

    17: (
        2.169,
        8.444,
        1.332
    )

}


class ArucoDestination(Node):

    def __init__(self):

        super().__init__('aruco_destination')

        self.bridge = CvBridge()

        self.diccionario = \
            cv2.aruco.getPredefinedDictionary(
                cv2.aruco.DICT_5X5_50
            )

        self.parametros = self.crear_parametros()

        if hasattr(cv2.aruco, 'ArucoDetector'):

            self.detector = cv2.aruco.ArucoDetector(
                self.diccionario,
                self.parametros
            )

        else:

            self.detector = None

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            qos_profile_sensor_data
        )

        self.publisher = self.create_publisher(
            Pose2D,
            '/destino_aruco',
            10
        )

        self.ultimo_id = None

        self.get_logger().info(
            'Detector de ArUcos iniciado'
        )

        self.get_logger().info(
            f'OpenCV {cv2.__version__}'
        )


    def crear_parametros(self):

        if hasattr(
            cv2.aruco,
            'DetectorParameters'
        ):

            parametros = \
                cv2.aruco.DetectorParameters()

        else:

            parametros = \
                cv2.aruco.DetectorParameters_create()


        parametros.errorCorrectionRate = 1.0

        parametros.maxErroneousBitsInBorderRate = 0.6

        parametros.perspectiveRemovePixelPerCell = 8

        parametros.perspectiveRemoveIgnoredMarginPerCell = \
            0.05

        parametros.adaptiveThreshWinSizeMin = 3
        parametros.adaptiveThreshWinSizeMax = 53
        parametros.adaptiveThreshWinSizeStep = 4

        parametros.minOtsuStdDev = 2.0


        if hasattr(
            cv2.aruco,
            'CORNER_REFINE_SUBPIX'
        ):

            parametros.cornerRefinementMethod = \
                cv2.aruco.CORNER_REFINE_SUBPIX


        if hasattr(
            parametros,
            'detectInvertedMarker'
        ):

            parametros.detectInvertedMarker = True


        return parametros


    def image_callback(self, msg):

        imagen = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        gris = cv2.cvtColor(
            imagen,
            cv2.COLOR_BGR2GRAY
        )


        if self.detector is not None:

            esquinas, ids, rechazados = \
                self.detector.detectMarkers(
                    gris
                )

        else:

            esquinas, ids, rechazados = \
                cv2.aruco.detectMarkers(
                    gris,
                    self.diccionario,
                    parameters=self.parametros
                )


        if ids is None:

            self.ultimo_id = None
            return


        id_aruco = int(
            ids[0][0]
        )


        if id_aruco not in DESTINOS:
            return


        x, y, gamma = \
            DESTINOS[id_aruco]


        destino = Pose2D()

        destino.x = x
        destino.y = y
        destino.theta = gamma


        self.publisher.publish(
            destino
        )


        if id_aruco != self.ultimo_id:

            self.get_logger().info(
                f'ArUco detectado: ID {id_aruco}'
            )

            self.get_logger().info(
                f'Destino: '
                f'x={x:.2f}, '
                f'y={y:.2f}, '
                f'gamma={gamma:.2f}'
            )

            self.ultimo_id = id_aruco


def main(args=None):

    rclpy.init(args=args)

    node = ArucoDestination()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
