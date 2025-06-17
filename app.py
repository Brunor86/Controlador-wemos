from flask import Flask, request, render_template, jsonify
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

# === Configuración MQTT desde variables de entorno ===
MQTT_BROKER = "10d5264920a243d0b583f5a78c15c5b4.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_TOPIC_BASE = "comandos/"

# === Dispositivos disponibles ===
DISPOSITIVOS = ["LUZ1", "LUZ2", "VENTILADOR", "BOMBA"]

# === Conexión MQTT ===
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

# === Rutas Flask ===

@app.route("/")
def home():
    return "Servidor Flask OK"

@app.route("/web")
def web():
    return render_template("index.html", dispositivos=DISPOSITIVOS)

@app.route("/encender/<dispositivo>")
def encender(dispositivo):
    if dispositivo in DISPOSITIVOS:
        client.publish(MQTT_TOPIC_BASE + dispositivo, "ON")
        return f"{dispositivo} encendido"
    return "Dispositivo no válido", 404

@app.route("/apagar/<dispositivo>")
def apagar(dispositivo):
    if dispositivo in DISPOSITIVOS:
        client.publish(MQTT_TOPIC_BASE + dispositivo, "OFF")
        return f"{dispositivo} apagado"
    return "Dispositivo no válido", 404

@app.route("/dispositivos")
def dispositivos():
    return jsonify(DISPOSITIVOS)

# === Ejecutar localmente (opcional) ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
