import mysql.connector

db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'sensor_monitoring',
}

def connect_db():
    return mysql.connector.connect(**db_config)
