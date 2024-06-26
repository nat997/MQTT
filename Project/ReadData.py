import mysql.connector
import pandas as pd
import streamlit as st
from db import connect_db

def get_data(query):
    try:
        db_connection = connect_db()
        df = pd.read_sql(query, db_connection)
        db_connection.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return pd.DataFrame()

def calculate_statistics(df, period='H'):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    if period == 'H':
        grouped_df = df.resample('H').agg({
            'temperature': ['mean', 'min', 'max', 'std'],
            'humidity': ['mean', 'min', 'max', 'std']
        })
    elif period == 'D':
        grouped_df = df.resample('D').agg({
            'temperature': ['mean', 'min', 'max', 'std'],
            'humidity': ['mean', 'min', 'max', 'std']
        })
    return grouped_df

def calculate_sensor_statistics(df, sensor_id, period='H'):
    df = df[df['sensor_id'] == sensor_id]
    return calculate_statistics(df, period)
