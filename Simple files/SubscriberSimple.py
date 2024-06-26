import paho.mqtt.client as mqtt

# Fonction de rappel appelée lors de la connexion au broker
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("exo1")  # S'abonner au topic "exo1"

# Fonction de rappel appelée lors de la réception d'un message
def on_message(client, userdata, msg):
    print(f"Message reçu sur le topic {msg.topic}: {msg.payload.decode()}")

# Création d'une instance de client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect  # Attacher la fonction on_connect
client.on_message = on_message  # Attacher la fonction on_message

# Connexion au broker MQTT
client.connect("51.38.185.58", 1883, 60)

# Boucle pour maintenir la connexion et traiter les messages
client.loop_forever()
