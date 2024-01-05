import bluetooth
import paho.mqtt.client as mqtt
import time
import threading
import functools

class Arduino:
    def __init__(self,ArduinoName,mqttAddress,mqttPort):
        self.name = ArduinoName
        self.address = None
        self.port = 1
        self.socket = None
        self.mqttAddress = mqttAddress
        self.mqttPort = mqttPort
        self.mqttClinet = mqtt.Client()
        __connectMqtt()

    def __connectMqtt(self):
        self.mqttClinet.connect(self.mqttAddress,self.mqttPort,60)

    def connect(self):
        nearDevice = bluetooth.discover_devices()
        for device in nearDevice:
            if self.name == bluetooth.lookup_name(device):
                self.address = device
                break
        
        if self.address is not None:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                self.socket.connect((self.address,self.port))
                print("Connected to Arduino")
            except Exception as e:
                print("Connection error:", e)
        else:
            print("Not find Arduino")
    
    def publish(self, topic):
        try:
            while True:
                data = self.socket.recv(1024).decode()
                if(data == 23221):
                    self.mqttClinet.publish(topic)
                else:
                    self.mqttClinet.publish(topic,data)
                print("Received data from Arduino:", data)
        except Exception as e:
            print("[ERROR]", e)

    
    def subscribe(self):
        try:
            while True:
                pass
        except Exception as e:
            print("[ERROR]",e)

def main():
    arduino = Arduino("Arara","192.168.137.35",1883)
    arduino.connect()

    pub = threading.Thread(target=functools.partial(arduino.publish, "Arduino/"))
    pub.daemon = True
    pub.start()
    

    while True:
        time.sleep(1)
        print("Still running...")

if __name__ == "__main__":
    main()