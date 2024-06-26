# IoT Weather Station Data Monitoring

This project is designed to monitor weather station data using MQTT for real-time data transmission and MySQL for data storage. Streamlit is used for visualizing the data.

## Project Structure

Project/
├── db.py
├── mqtt_client.py
├── data_retrieval.py
├── app.py
└── main.py


## Modules

- **db.py**: Handles the MySQL database connection.
- **mqtt_client.py**: Manages the MQTT client and the database operations related to it.
- **data_retrieval.py**: Provides a function to retrieve data from the database.
- **app.py**: The Streamlit application for data visualization.
- **main.py**: Entry point to start the MQTT client.

## Setup Instructions

### Prerequisites

- Python 3.x
- MySQL
- MQTT broker (e.g., [mqtt-dashboard.com](http://mqtt-dashboard.com))

