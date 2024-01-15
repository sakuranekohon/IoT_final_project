#!/usr/bin/env python3
import rospy
import paho.mqtt.client as mqtt
import threading
import time
from std_msgs.msg import String

class Broker:
    def __init__(self,mqttAddress,mqttPort,mqttTopic):
        self.mqttAddress = mqttAddress
        self.mqttPort = mqttPort
        self.mqttTopic = mqttTopic
        self.mqttClient = mqtt.Client()
        

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if(rc == 0):
                print("Broker success connect mqtt server")
                self.mqttClient.subscribe(self.mqttTopic)
            else:
                print("Connect failed")
        self.mqttClient.on_connect = on_connect
        self.mqttClient.connect(self.mqttAddress,self.mqttPort,60)
        self.mqttClient.loop_start()

        rospy.init_node("Broker",anonymous=True)
        rospy.loginfo("Create node name Duckiebot")

    def mqttToRos(self):
        pub = rospy.Publisher("Arduino/data",String,queue_size=10)
        def on_message(client,userdata,msg):
            ArduinoData = str(msg.payload.decode("utf-8"))
            rospy.loginfo("ArduinoData = " + ArduinoData)
            pub.publish(ArduinoData)
            
        self.mqttClient.on_message = on_message

    def rosToMqtt(self):
        def on_message(data):
            rospy.loginfo("DuckiebotData = " + data.data)
            self.mqttClient.publish("Duckiebot/data",str(data.data))

        rospy.Subscriber("Duckiebot/data",String,on_message)
        rospy.spin()

def main():
    broker = Broker("192.168.137.35",1883,"Arduino/data")
    broker.connect()
    
    MTR = threading.Thread(target=broker.mqttToRos)
    MTR.daemon =True
    MTR.start()

    RTM = threading.Thread(target=broker.rosToMqtt)
    RTM.daemon = True
    RTM.start()

    rospy.spin()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInitException as e:
        print("[ERROR]ROS :",e)