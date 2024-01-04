import bluetooth
import paho.mqtt.client as mqclient
import time
import threading
import functools

class Arduino:
    def __init__(self,ArduinoName):
        self.name = ArduinoName
        self.address = None
        self.port = 1
        self.socket = None

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
                print("Received data from Arduino:", data)
        except Exception as e:
            print("[Error]", e)

    
    def subscribe(self):
        pass

def main():
    arduino = Arduino("Arara")
    arduino.connect()

    pub = threading.Thread(target=functools.partial(arduino.publish, "your_topic"))
    pub.daemon = True
    pub.start()


    while True:
        time.sleep(1)
        print("Still running...")

if __name__ == "__main__":
    main()