import paho.mqtt.client as mqtt
import json
from db import connect_db

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor_data/#")  # Subscribe to all sensors

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    try:
        data = json.loads(msg.payload)
        sensor_id = data['sensor_id']
        location = data['location']
        temperature = data.get('temperature')
        humidity = data.get('humidity')

        # Insert data into MySQL, ignore duplicates
        global db_connection
        cursor = db_connection.cursor()
        cursor.execute("""
            INSERT INTO sensors (sensor_id, location, temperature, humidity, timestamp) 
            VALUES (%s, %s, %s, %s, NOW())
        """, (sensor_id, location, temperature, humidity))
        db_connection.commit()
        cursor.close()
        print("Data inserted into database successfully.")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing message: {e}")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        # Reconnect if connection to MySQL is lost
        db_connection = connect_db()

# Initialize the global database connection
db_connection = connect_db()

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.mqttdashboard.com", 1883, 60)
    client.loop_forever()
