import streamlit as st
import plotly.express as px
from ReadData import get_data

# Streamlit app
st.title('IoT Weather Station Data')

# Tabs
tab1, tab2 = st.tabs(["Plot", "Data Table"])

with tab1:
    st.header("Temperature and Humidity Over Time")
    df = get_data("SELECT * FROM sensors ORDER BY timestamp DESC")
    if not df.empty:
        fig = px.line(df, x='timestamp', y=['temperature', 'humidity'], color='sensor_id', labels={'value': 'Measurements'}, title="Temperature and Humidity Over Time")
        st.plotly_chart(fig)
    else:
        st.write("No data available.")

with tab2:
    st.header("Raw Data")
    df = get_data("SELECT * FROM sensors ORDER BY timestamp DESC")
    if not df.empty:
        st.write(df)
    else:
        st.write("No data available.")
