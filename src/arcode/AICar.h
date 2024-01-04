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

#include <Arduino.h>
#include <SoftwareSerial.h>

struct Distance {
    byte noSafeDistance;
    byte normalDistance;
};

struct Lane {
    byte currentLane;
    byte laneSize;
    bool direction;
  };

class AICar {
private:
  byte speed;
  Distance distance;
  Lane lane;
  bool isCarStop;
public:
  SoftwareSerial* BTSerial; 
  AICar(byte speed, byte noSafeDistance, byte normalDistance, byte currentlane, byte laneSize, bool direction);
  void setSpeed(byte speed);
  void setNoSafeDistance(byte noSafeDistance);
  void setNormalDistance(byte normalDistance);
  void setCurrentLane(byte currentLane);
  void setLaneSize(byte laneSize);
  void setLaneDirection(bool direction);
  void setCarStatus(bool stop);
  byte getSpeed();
  Distance getDistance();
  Lane getLane();
  bool getCarStatus();
  void init();
  void move(bool isFront);
  void stop(bool isUrgent);
  void switchLanes(bool isLeft, byte offset);
  void publisher(byte carDistance);
  String subscriber();
  byte calDistance();
};

#endif