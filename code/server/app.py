from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from proFunc import testCurrP, testCarStats, testTarget
import paho.mqtt.client as mqtt
import eventlet

eventlet.monkey_patch()
app = Flask(__name__)
socketio = SocketIO(app)
MQTT_TOPIC = [("test/Target", 0), ("test/CurrP", 0)]

viaPath = list()
carP = tuple()

def messageFunction (client, userdata, message):
    global carP
    topic = message.topic
    msg = str(message.payload.decode("utf-8"))

    if topic == "test/CurrP":
        carP = testCurrP(msg)
        carP1 = str(carP)
        carP1 = carP1.replace("(","[")
        carP1 = carP1.replace(")","]")
        print(carP1)
        socketio.emit('carP', carP1)

mqttClient = mqtt.Client()
# mqttClient.connect("192.168.50.100", 1883)
mqttClient.connect("192.168.50.212", 1883)
mqttClient.subscribe(MQTT_TOPIC)
mqttClient.on_message = messageFunction
mqttClient.loop_start()

@app.route('/',methods = ['GET','POST'])
def index():
    global viaPath, carP

    if request.method == 'POST':
        msg = request.form['target']
        viaPath = testTarget(msg, viaPath, carP)
        print("viaPath: ", viaPath)

        if not isinstance(viaPath, list):
            return render_template("index.html", err = viaPath)

        msg = str(viaPath)
        mqttClient.publish("test/Route", msg)

        return render_template("index.html")
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
