import json
import random
import paho.mqtt.client as mqtt

# Générer une liste de 4 nombres aléatoires
data = [random.randint(1, 100) for _ in range(4)]

# Convertir la liste en JSON
json_data = json.dumps(data)

# Fonction de rappel pour la publication
def on_publish(client, userdata, mid):
    print(f"Message {mid} envoyé")

# Création du client MQTT
client = mqtt.Client()
client.on_publish = on_publish

# Connexion au broker
client.connect("51.38.185.58", 1883, 60)

# Publication du message JSON sur le topic "ingestionAB"
topic = "ingestionAB"
result = client.publish(topic, json_data)

# Assurer que le message est publié avant de quitter
result.wait_for_publish()

# Déconnexion
client.disconnect()
