#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from mqtt_bridge import MqttPublisher

def ros_callback(data):
    # ROS訊息到MQTT訊息的轉換
    mqtt_pub.publish(data.data)

if __name__ == '__main__':
    rospy.init_node('ros_to_mqtt_publisher')

    # ROS訊息的訂閱者
    rospy.Subscriber('your_ros_topic', String, ros_callback)

    # MQTT發布者
    mqtt_pub = MqttPublisher()
    mqtt_pub.connect('mqtt_broker_address', 'mqtt_topic')  # 設定MQTT broker和topic

    rospy.spin()
