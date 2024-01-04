#include "AICar.h"

AICar::AICar(byte speed, byte noSafeDistance, byte normalDistance,byte currentLane,byte laneSize,bool direction){
  this->speed = speed;
  this->distance.noSafeDistance = noSafeDistance;
  this->distance.normalDistance = normalDistance;
  this->lane.currentLane = currentLane;
  this->lane.laneSize = laneSize;
  this->lane.direction = direction;
  this->BTSerial = new SoftwareSerial(10, 11);
}

void AICar::setSpeed(byte speed) {
  this->speed = speed;
}

void AICar::setNoSafeDistance(byte noSafeDistance) {
  this->distance.noSafeDistance = noSafeDistance;
}

void AICar::setNormalDistance(byte normalDistance) {
  this->distance.normalDistance = normalDistance;
}

void AICar::setCurrentLane(byte currentLane){
  this->lane.currentLane = currentLane;
}

void AICar::setLaneSize(byte laneSize){
  this->lane.laneSize = laneSize;
}

void AICar::setLaneDirection(bool direction){
  this->lane.direction = direction;
}

void AICar::setCarStatus(bool stop){
  this->isCarStop = stop;
}

byte AICar::getSpeed() {
  return this->speed;
}

Distance AICar::getDistance() {
  return this->distance;
}

Lane AICar::getLane(){
  return this->lane;
}

bool AICar::getCarStatus(){
  return this->isCarStop;
}

void AICar::init() {
  /*motor pin status set*/
  pinMode(LPWM, OUTPUT);
  pinMode(LINF, OUTPUT);
  pinMode(LINB, OUTPUT);
  pinMode(RPWM, OUTPUT);
  pinMode(RINF, OUTPUT);
  pinMode(RINB, OUTPUT);

  /*Sensors pin et*/
  pinMode(ECHO, INPUT);
  pinMode(TRIG, OUTPUT);

  Serial.print("speed = ");
  Serial.print(speed);
  Serial.print(", not safe distance = ");
  Serial.print(distance.noSafeDistance);
  Serial.print(", normal distance = ");
  Serial.print(distance.normalDistance);
  Serial.println("Start in five seconds");
  
   BTSerial->begin(38400);

  isCarStop = false;
  int cnt = 5;
  for (int i = cnt; i > 0; i--) {
    Serial.print(i);
    Serial.println("...");
    delay(1000);
  }
  Serial.println("Start");
}

void AICar::move(bool isFront) {
  digitalWrite(LINF, isFront);
  digitalWrite(LINB, !isFront);
  digitalWrite(RINF, isFront);
  digitalWrite(RINB, !isFront);

  analogWrite(LPWM, speed);
  analogWrite(RPWM, speed);
}

void AICar::stop(bool isUrgent) {
  if (isUrgent) {
    digitalWrite(LINF, LOW);
    digitalWrite(LINB, LOW);
    digitalWrite(RINF, LOW);
    digitalWrite(RINB, LOW);
  } else {
    for (int i = speed; i > 0; i -= 10) {
      setSpeed(i);
      move(true);
    }
    digitalWrite(LINF, LOW);
    digitalWrite(LINB, LOW);
    digitalWrite(RINF, LOW);
    digitalWrite(RINB, LOW);
  }
  isCarStop = true;
}

void AICar::switchLanes(bool isLeft, byte offset) {
  if (isLeft) {
    analogWrite(RPWM, speed + offset);
    delay(10);
    move(true);
    delay(30);
    analogWrite(LPWM, speed + offset);
  } else {
    analogWrite(LPWM, speed + offset);
    delay(10);
    move(true);
    delay(30);
    analogWrite(RPWM, speed + offset);
  }
}

void AICar::publisher(byte carDistance) {
  String message = String(carDistance) + String(lane.laneSize) + String(lane.currentLane);
  Serial.println(message);
  if (carDistance == 1000)
    BTSerial->println("A");
  else
    BTSerial->println(message);
}

String AICar::subscriber() {
  String data;
  if(BTSerial->available()){
    char c;
    while((c = BTSerial->read()) != '\n'){
      data += c;
    }
  }
  return data;
}

byte AICar::calDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  float udistance = pulseIn(ECHO, HIGH) / 58;

  return (byte)udistance;
}
