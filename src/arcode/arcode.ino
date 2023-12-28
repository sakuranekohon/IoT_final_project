#include "AICar.h"

AICar car(150,8,20);

void setup() {
  Serial.begin(9600);
  car.init();
}

void loop() {
  // put your main code here, to run repeatedly:

}
