CREATE DATABASE sensor_monitoring;

USE sensor_monitoring;

CREATE TABLE sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    UNIQUE(sensor_id, timestamp)  
);
