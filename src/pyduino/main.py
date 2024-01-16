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

        def on_connect(client, userdata, flags, rc):
            if(rc == 0):
                print("Connect to MQTT server")
                self.mqttClinet.subscribe("Duckiebot/data")
            else:
                print("Connect failed")

        self.mqttClinet.on_connect = on_connect
        self.mqttClinet.connect(self.mqttAddress,self.mqttPort,60)
        self.mqttClinet.loop_start()
    
    def publish(self, topic):
        try:
            while True:
                data = self.socket.recv(1024).decode()
                #print("Received data from Arduino:", data)
                if(data == "23221"):
                    self.mqttClinet.publish(topic,"000")
                else:
                    self.mqttClinet.publish(topic,str(data))
        except Exception as e:
            print("[ERROR]", e)

    
    def subscribe(self):
        def on_message(client,userdata,msg):
            duckieData = str(msg.payload.decode("utf-8"))
            print("Duckiebot Node : ",duckieData)
            
            self.socket.send(duckieData.encode() + b'\n')
        
        self.mqttClinet.on_message = on_message

    def disconnect(self):
        self.socket.close()

def check_input():
    while True:
        user_input = input()  # 等待終端輸入
        if user_input.lower() == "exit":  # 如果輸入了 "exit"，程式就會結束
            break

def main():
    arduino = Arduino("Arara","192.168.137.35",1883)
    arduino.connect()

    pub = threading.Thread(target=functools.partial(arduino.publish, "Arduino/data"))
    pub.daemon = True
    pub.start()

    sub = threading.Thread(target=arduino.subscribe)
    sub.daemon = True
    sub.start()

    input_thread = threading.Thread(target=check_input)
    input_thread.daemon = True
    input_thread.start()


    while True:
        time.sleep(1)

    arduino.disconnect()

if __name__ == "__main__":
    main()