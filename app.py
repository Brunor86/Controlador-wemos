from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

# Configuración MQTT
MQTT_BROKER = "10d5264920a243d0b583f5a78c15c5b4.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_TOPIC_BASE = "comandos/"

DISPOSITIVOS = ["LUZ1", "LUZ2", "VENTILADOR", "BOMBA"]

# Estado inicial de los dispositivos
estado_dispositivos = {disp: "OFF" for disp in DISPOSITIVOS}

# Conexión MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

@app.route("/")
def home():
    return "Servidor Flask OK"

@app.route("/web")
def web():
    return render_template("index.html", dispositivos=DISPOSITIVOS, estados=estado_dispositivos)

@app.route("/encender/<dispositivo>")
def encender(dispositivo):
    if dispositivo in DISPOSITIVOS:
        client.publish(MQTT_TOPIC_BASE + dispositivo, "ON")
        estado_dispositivos[dispositivo] = "ON"
        return jsonify({"status": "ok", "mensaje": f"{dispositivo} encendido"})
    return jsonify({"status": "error", "mensaje": "Dispositivo no válido"}), 404

@app.route("/apagar/<dispositivo>")
def apagar(dispositivo):
    if dispositivo in DISPOSITIVOS:
        client.publish(MQTT_TOPIC_BASE + dispositivo, "OFF")
        estado_dispositivos[dispositivo] = "OFF"
        return jsonify({"status": "ok", "mensaje": f"{dispositivo} apagado"})
    return jsonify({"status": "error", "mensaje": "Dispositivo no válido"}), 404

@app.route("/estado")
def estado():
    return jsonify(estado_dispositivos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
