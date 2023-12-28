#include "AICar.h"

AICar::AICar(byte speed,byte noSafeDistance,byte normalDistance){
  this->speed = speed;
  this->distance[0] = noSafeDistance;
  this->distance[1] = normalDistance;
}

void AICar::setSpeed(byte speed){
  this->speed = speed;
}

void AICar::setNoSafeDistance(byte noSafeDistance){
  this->distance[0] = noSafeDistance;
}

void AICar::setNormalDistance(byte normalDistance){
  this->distance[1] = normalDistance;
}

byte AICar::getSpeed(){
  return this->speed;
}

byte AICar::getNoSafeDistance(){
  return this->distance[0];
}

byte AICar::getNormalDistance(){
  return this->distance[1];
}

void AICar::init(){
  /*motor pin status set*/
  pinMode(LPWM,OUTPUT);
  pinMode(LINF,OUTPUT);
  pinMode(LINB,OUTPUT);
  pinMode(RPWM,OUTPUT);
  pinMode(RINF,OUTPUT);
  pinMode(RINB,OUTPUT);

  /*Sensors pin et*/
  pinMode(ECHO,INPUT);
  pinMode(TRIG,OUTPUT);

  Serial.print("speed = ");
  Serial.print(speed);
  Serial.print(", not safe distance = ");
  Serial.print(distance[0]);
  Serial.print(", normal distance = ");
  Serial.print(distance[1]);
  Serial.println("Start in five seconds");

  btSerial.begin(9600);

  nh.initNode();
  nh.advertise(pub);
  nh.subscriber(sub);

  int cnt = 5;
  for(int i = cnt;i > 0;i--){
    Serial.print(cnt);
    Serial.println("...");
    delay(1000);
  }
  Serial.println("Start");
}

void AICar::move(bool isFront){
  digitalWrite(LINF,isFront);
  digitalWrite(LINB,!isFront);
  digitalWrite(RINF,isFront);
  digitalWrite(RINB,!isFront);

  analogWrite(LPWM,speed);
  analogWrite(RPWM,speed);
}

void AICar::stop(bool isUrgent){
  if(isUrgent){
    digitalWrite(LINF,LOW);
    digitalWrite(LINB,LOW);
    digitalWrite(RINF,LOW);
    digitalWrite(RINB,LOW);
  }else{
    for(int i = speed;i>0;i-=10){
      setSpeed(i);
      move(true);
    }
    digitalWrite(LINF,LOW);
    digitalWrite(LINB,LOW);
    digitalWrite(RINF,LOW);
    digitalWrite(RINB,LOW);
  }
}

void AICar::switchLanes(bool isLeft,byte offset){
  time = millis();
  if(isLeft){
    analogWrite(RPWM,speed+offset);
    delay(10);
    move(true);
    delay(30);
    analogWrite(LPWM,speed+offset);
  }esle{
    analogWrite(LPWM,speed+offset);
    delay(10);
    move(true);
    delay(30);
    analogWrite(RPWM,speed+offset);
  }
}

void AICar::publisher(){

}

string AICar::subscriber(){

}

byte AICar::calDistance(){
  digitalWrite(TRIG,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG,LOW);
  float udistance = pulseIn(ECHO,HIGH)/58;
  
  return (byte) udistance;
}
