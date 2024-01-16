#include "AICar.h"

AICar car(30, 8, 30, 1, 2, 1);

void setup() {
  Serial.begin(9600);
  car.init();
}
String rosData = "000";

void loop() {
  
  rosData = car.subscriber();
  
  if (!car.getCarStatus()) {
    car.move(1);
    //收到000以外表示前方有車禍、檢查車禍是否在同車道
    if (rosData != "000" || byte(rosData[2]) == car.getLane().currentLane) {
      if (rosData[0] == '1') {
        car.stop(1);
      } else if (rosData[0] == '2') {
        car.stop(0);
      } else {
        byte laneSize = byte(rosData[1]);
        byte occLane = byte(rosData[2]);
        if (laneSize == 1) {
          car.stop(1);
        } else {
          byte offset = 30;
          if (occLane - 1 > 0) {
            car.switchLanes(1, offset);
          } else if (occLane + 1 < laneSize) {
            car.switchLanes(0, offset);
          }
        }
      }
    }

    int carCD = car.calDistance();
    //車禍檢測
    if (carCD <= car.getDistance().noSafeDistance) {
      String sendRosData = String(1) + String(car.getLane().laneSize) + String(car.getLane().currentLane);
      car.publisher(1);
      car.stop(1);
      car.setCarStatus(1);
      delay(1000);
    }else{
      car.publisher(10);
    }
  } else {
    car.stop(1);
    delay(1000);
    if (car.calDistance() > 30)
      car.setCarStatus(0);
  }
}
