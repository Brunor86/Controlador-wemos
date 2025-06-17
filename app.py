from flask import Flask, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Datos del broker MQTT (HiveMQ Cloud o Mosquitto en local)
MQTT_BROKER = "10d5264920a243d0b583f5a78c15c5b4.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "brunorossini02@gmail.com"
MQTT_PASS = "Bruno32105654"
MQTT_TOPIC_BASE = "comandos/"

# Crear cliente MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()  # Usar TLS
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

@app.route("/")
def home():
    return "Servidor Flask OK"

@app.route("/encender/<dispositivo>")
def encender(dispositivo):
    client.publish(MQTT_TOPIC_BASE + dispositivo, "ON")
    return f"{dispositivo} encendido"

@app.route("/apagar/<dispositivo>")
def apagar(dispositivo):
    client.publish(MQTT_TOPIC_BASE + dispositivo, "OFF")
    return f"{dispositivo} apagado"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
