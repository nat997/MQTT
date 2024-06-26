import json
import paho.mqtt.client as mqtt

# Fonction de rappel pour la connexion
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connecté avec le code {reason_code}")
    client.subscribe("ingestionAB")

# Fonction de rappel pour la réception de messages
def on_message(client, userdata, msg):
    # Convertir le payload JSON en liste de nombres
    data = json.loads(msg.payload.decode())
    print(f"Message reçu sur le topic {msg.topic}: {data}")

    # Calculer la somme des nombres
    result = sum(data)
    print(f"Somme calculée: {result}")

    # Envoyer le résultat sur le topic "resultAB"
    result_topic = "resultAB"
    client.publish(result_topic, json.dumps({"result": result}))

# Création du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker
client.connect("51.38.185.58", 1883, 60)

# Boucle pour maintenir la connexion et traiter les messages
client.loop_forever()
