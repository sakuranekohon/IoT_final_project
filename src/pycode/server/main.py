import serial
import paho.mqtt.client as mqtt 

def receiverArduino(serial_port, baud_rate):
    # 建立串口物件
    ser = serial.Serial(serial_port, baud_rate)
    data = None

    if ser.in_waiting > 0:
        data = ser.readline().decode("utf-8").rstrip()

    ser.close()  # 確保在使用完後關閉串口
    return data

def mqttPub(broker_address, broker_port, topic, data):
    client = mqtt.Client()
    try:
        client.connect(broker_address, broker_port, keepalive=60)
        client.publish(topic, data)
        client.disconnect()  # 完成上傳後斷開MQTT連接
    except Exception as e:
        print(f"MQTT publish error: {e}")

def main():
    serial_port = 'COM3'  # 修改為你的串口號
    baud_rate = 38400 
    broker_address = '192.168.137.35'  # 修改為你的MQTT broker位址
    broker_port = 1883 
    mqtt_topic = "ArduinoTopic"  # 修改為你想要上傳的MQTT主題

    while True:
        data = receiverArduino(serial_port, baud_rate)
        if data is not None:
            mqttPub(broker_address, broker_port, mqtt_topic, data)

if __name__ == "__main__":
    main()
