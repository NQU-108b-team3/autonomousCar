from movLocal import mov
import paho.mqtt.client as mqtt
import time

mqttClient = mqtt.Client()

currentP = (16, 5)
viaPath = list()
nextP = tuple()
carMov = 0

def messageFunction (client, userdata, message):
    global viaPath, carMov
    topic = message.topic
    msg = str(message.payload.decode("utf-8"))

    if topic == "test/Route":
        viaPath = list(eval(msg))
        print("via Path: ", viaPath)
        carMov = 1

# mqttClient.connect("192.168.50.100", 1883)
mqttClient.connect("192.168.50.212", 1883)
# mqttClient.connect("192.168.0.107", 1883)
mqttClient.subscribe("test/Route")
mqttClient.on_message = messageFunction
mqttClient.loop_start()

while True:
    if carMov == 1:
        currentP = mov(mqttClient, currentP, viaPath)
        nextP = tuple()
        viaPath = list()
        carMov = 0
    else:        
        msg = str(currentP)
        mqttClient.publish("test/CurrP", msg)
        time.sleep(1)
