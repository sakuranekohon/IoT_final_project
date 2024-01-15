#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import WheelsCmdStamped,Twist2DStamped
from sensor_msgs.msg import CameraInfo, CompressedImage
from ultralytics import YOLO
from rospkg import RosPack
from cv_bridge import CvBridge
import time

# throttle and direction for each wheel
THROTTLE_LEFT = 0.5        
DIRECTION_LEFT = 1         
THROTTLE_RIGHT = 0.5   
DIRECTION_RIGHT = -1       


class WheelControlNode(DTROS):
    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(WheelControlNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # static parameters
        vehicle_name = os.environ['VEHICLE_NAME']
        wheels_topic = f"/{vehicle_name}/wheels_driver_node/wheels_cmd"
        # form the message
        self._vel_left = THROTTLE_LEFT * DIRECTION_LEFT
        self._vel_right = THROTTLE_RIGHT * DIRECTION_RIGHT
        # construct publisher
        self._publisher = rospy.Publisher(wheels_topic, WheelsCmdStamped, queue_size=1)

    def run(self):
        # publish 10 messages every second (10 Hz)
        rate = rospy.Rate(0.1)
        while not rospy.is_shutdown():
            message = WheelsCmdStamped(vel_left=self._vel_left, vel_right=self._vel_right)
            self._publisher.publish(message)
            rate.sleep()

    def updataLeftWheel(self,throttle,direction):
        global THROTTLE_LEFT,DIRECTION_LEFT
        THROTTLE_LEFT = throttle
        DIRECTION_LEFT = direction

    def updataRightWheel(self,throttle,direction):
        global THROTTLE_RIGHT,DIRECTION_RIGHT
        THROTTLE_RIGHT = throttle
        DIRECTION_RIGHT = direction

    def on_shutdown(self):
        stop = WheelsCmdStamped(vel_left=0, vel_right=0)
        self._publisher.publish(stop)

class SwitchLane:
    def __init__(self,nodeName):
        self.wheelNode = WheelControlNode(nodeName)
        self.wheelNode.run()

    def left(self):
        self.wheelNode.updataRightWheel(0.8,-1)
        self.wheelNode.updataLeftWheel(0.3,1)
        time.sleep(0.05)
        self.wheelNode.updataRightWheel(0.5,-1)
        self.wheelNode.updataLeftWheel(0.5,1)
        time.sleep(0.05)
        self.wheelNode.updataRightWheel(0.3,-1)
        self.wheelNode.updataLeftWheel(0.8,1)

    def right(self):
        self.wheelNode.updataRightWheel(0.3,-1)
        self.wheelNode.updataLeftWheel(0.8,1)
        time.sleep(0.05)
        self.wheelNode.updataRightWheel(0.5,-1)
        self.wheelNode.updataLeftWheel(0.5,1)
        time.sleep(0.05)
        self.wheelNode.updataRightWheel(0.8,-1)
        self.wheelNode.updataLeftWheel(0.3,1)

class CameraNode(DTROS):
    def __init__(self):
        super(CameraNode, self).__init__(node_name='camera_node', node_type=NodeType.GENERIC)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/camera_node/image/compressed', CompressedImage, self.image_callback)
        self.cmd_pub = rospy.Publisher('/duckiebot/wheels_driver_node/car_cmd', Twist2DStamped, queue_size=1)

        # Load YOLO model
        ros_pack = RosPack()
        model_path = ros_pack.get_path("duckie") + "/model/best.pt"
        self.yolo = YOLO(model_path)
        self.bbox = None

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

            results = self.yolo(cv_image)

            if results and results[0].boxes:
                self.bbox = results[0].boxes
            else:
                self.bbox = None

        except Exception as e:
            rospy.logerr(f"Error: {e}")