#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

#ros pub test
if __name__ =='__main__':
    rospy.init_node('duckie',anonymous=True)
    pub = rospy.Publisher('Duckiebot/data',String,queue_size=10)
    rate = rospy.Rate(1)

    cnt = 0
    while not rospy.is_shutdown():
        hello ="hello world !" + str(cnt)
        pub.publish(hello)
        rospy.loginfo(hello)
        cnt+=1
        rate.sleep()