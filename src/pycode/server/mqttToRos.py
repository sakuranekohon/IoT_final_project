#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from mqtt_bridge import MqttSubscriber

def mqtt_callback(data):
    # MQTT訊息到ROS訊息的轉換
    rospy.loginfo(data.payload)
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.payload)
    ros_pub.publish(data.payload)

if __name__ == '__main__':
    rospy.init_node('mqtt_to_ros_subscriber')

    # MQTT訂閱者
    mqtt_sub = MqttSubscriber()
    mqtt_sub.connect('mqtt_broker_address', 'mqtt_topic', mqtt_callback)  # 設定MQTT broker和topic

    # ROS發布者
    ros_pub = rospy.Publisher('your_ros_topic', String, queue_size=10)

    rospy.spin()
