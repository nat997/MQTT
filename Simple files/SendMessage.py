import json
import paho.mqtt.client as mqtt

# Données à envoyer
data = {
    "temperature anh tien": 22
}

# Convertir le dictionnaire en JSON
json_data = json.dumps(data)

# Fonction de rappel pour la publication
def on_publish(client, userdata, mid):
    print(f"Message {mid} envoyé")

# Création du client MQTT
client = mqtt.Client()
client.on_publish = on_publish

# Connexion au broker
client.connect("51.38.185.58", 1883, 60)

# Publication du message JSON
topic = "exo1"
result = client.publish(topic, json_data)

# Assurer que le message est publié avant de quitter
result.wait_for_publish()

# Déconnexion
client.disconnect()
