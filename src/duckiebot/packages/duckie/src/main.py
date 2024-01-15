#!/usr/bin/env python3

import time
import rospy
from std_msgs.msg import String

def on_message(data):
    ArduinoData = data.data
    if ArduinoData != "000" or ArduinoData[2] == 
    

def main():
    rospy.init_node("arduino_subscriber", anonymous=True)
    rospy.Subscriber("Arduino/data",String,on_message)

    rospy.spin()

if __name__ == "__main__":
    main()