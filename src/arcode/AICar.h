#ifndef AICAR_H
#define AICAR_H

/*Motor pin set*/
#define LPWM 6  //Left motor speed
#define LINF A0 //Left motor forward
#define LINB A1 //Left motor backward
#define RPWM 5  //Rigth motor speed
#define RINF A3 //Right motor forward
#define RINB A2 //Rigth motor backward

/*Sensors pin et*/
#define NUM_SENSORS 5
#define ECHO 2
#define TRIG 3

/*RX TX set*/
#define RX_PIN 1
#define TX_PIN 0

#include <Arduino.h>
#include <SoftwareSerial.h>
#include <ros.h>
#include <std_msg/Int8.h>

class AICar{
  private:
    ros::NodeHandle nh;
    byte speed;
    byte distance[2];
    SoftwareSerial btSerial(RX_PIN,TX_PIN);
    std_msgs::Int8 pub_msg;
    ros::Subsrciber<std_msgs::Int8> sub("publisher_topic",&);
    ros::Publisher pub("subscriber_topic",&pub_msg);
  public:
    AICar(byte speed,byte noSafeDistance,byte normalDistance);
    void setSpeed(byte speed);
    void setNoSafeDistance(byte noSafeDistance);
    void setNormalDistance(byte normalDistance);
    byte getSpeed();
    byte getNoSafeDistance();
    byte getNormalDistance();
    void init();
    void openMotor();
    void move();
    void stop(bool isUrgent);
    void switchLanes(bool isLeft);
    void publisher();
    void subscriber();
    byte calDistance();
};

#endif