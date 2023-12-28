#ifndef AICAR_H
#define AICAR_H

/*Motor pin set*/
#define LPWM 6   //Left motor speed
#define LINF A0  //Left motor forward
#define LINB A1  //Left motor backward
#define RPWM 5   //Rigth motor speed
#define RINF A3  //Right motor forward
#define RINB A2  //Rigth motor backward

/*Sensors pin set*/
#define NUM_SENSORS 5
#define ECHO 2
#define TRIG 3

/*RX TX set*/
#define RX_PIN 1
#define TX_PIN 0

#include <Arduino.h>
#include <SoftwareSerial.h>
#include <ros.h>
#include <std_msgs/String.h>

class AICar {
private:
  ros::NodeHandle nh;
  byte speed;
  byte distance[2];
  SoftwareSerial btSerial;
  String sub_str;
  /*create ROS publisher and subscriber*/
  std_msgs::String pub_msg;
  ros::Publisher pub;
  ros::Subscriber<std_msgs::String> sub;

  void subscriber(const std_msgs::String& sub_msg);
public:
  AICar(byte speed, byte noSafeDistance, byte normalDistance);
  void setSpeed(byte speed);
  void setNoSafeDistance(byte noSafeDistance);
  void setNormalDistance(byte normalDistance);
  byte getSpeed();
  byte getNoSafeDistance();
  byte getNormalDistance();
  void init();
  void move(bool isFront);
  void stop(bool isUrgent);
  void switchLanes(bool isLeft);
  void publisher(byte carDistance, byte laneSize, byte occLane);
  byte calDistance();
};

#endif