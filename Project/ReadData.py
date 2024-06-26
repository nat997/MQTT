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
