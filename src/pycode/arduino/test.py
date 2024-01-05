import paho.mqtt.client as mqtt
import time

# 回调函数 - 连接成功时调用
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def main():
    # 初始化 MQTT 客户端
    client = mqtt.Client()
    # 设置连接成功的回调函数
    client.on_connect = on_connect
    # 连接 MQTT 代理（此处为示例，需要修改为你的 MQTT 代理地址和端口号）
    client.connect("192.168.88.21", 1883, 60)

    # 开启一个循环以保持连接
    client.loop_start()

    # 发布消息到指定主题（此处为示例，可以根据需要发布消息）
    while True:
        # 发布消息到指定主题
        client.publish("test/hello", "Hello MQTT")
        time.sleep(1)  # 延时一秒

if __name__ == "__main__":
    main()
