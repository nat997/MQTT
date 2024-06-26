import streamlit as st
import sys
from PIL import Image, ExifTags
from transformers import pipeline
import mysql.connector
import pandas as pd
from ml_analysis import generate_caption_and_detect_disease
from ReadData import get_data
import plotly.express as px

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Plot", "Data Table", "ML", "Statistics"])

with tab1:
    st.header("Temperature and Humidity Over Time")
    df = get_data("SELECT * FROM sensors ORDER BY timestamp DESC")
    if not df.empty:
        df_melted = df.melt(id_vars=['timestamp', 'sensor_id'], value_vars=['temperature', 'humidity'],
                            var_name='type', value_name='value')
        df_melted['sensor_type'] = df_melted['sensor_id'] + '_' + df_melted['type']
        fig = px.line(df_melted, x='timestamp', y='value', color='sensor_type',
                      labels={'value': 'Measurements'}, title="Temperature and Humidity Over Time")
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

with tab3:
    st.header("ML")
    # Upload d'image
    uploaded_image = st.file_uploader("Choisissez une image de plante...", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)

        # Obtenir et afficher la taille de l'image
        width, height = image.size
        if width > 1200 or height > 1200:
            try:
                exif = image._getexif()
                if exif is not None:
                    orientation_key = next((key for key, value in ExifTags.TAGS.items() if value == 'Orientation'), None)
                    if orientation_key is not None and orientation_key in exif:
                        orientation = exif[orientation_key]
                        if orientation == 3:
                            image = image.rotate(180, expand=True)
                        elif orientation == 6:
                            image = image.rotate(270, expand=True)
                        elif orientation == 8:
                            image = image.rotate(90, expand=True)
                        # Affichage de l'image uploadée
                        width, height = image.size
                        st.write(f"Largeur: {width} pixels, Hauteur: {height} pixels")
                        st.image(image, caption='Image Uploadée', use_column_width=True)
            except Exception as e:
                st.write(f"Erreur lors de la correction de l'orientation: {e}")
                pass
            image = image.resize((224, 224))    
        else:
            # Affichage de l'image uploadée
            width, height = image.size
            st.write(f"Largeur: {width} pixels, Hauteur: {height} pixels")
            st.image(image, caption='Image Uploadée', use_column_width=True)
        
        # Placeholder pour le bouton ou le message de chargement
        button_placeholder = st.empty()

        # Si le bouton est cliqué
        if button_placeholder.button('Analyser l\'image'):
            # Affichage du spinner et du message pendant le traitement
            with st.spinner('En cours d\'exécution...'):
                caption, diseases = generate_caption_and_detect_disease(image)
                
                # Remplacement du spinner par les résultats une fois le traitement terminé
                with st.expander("Voir les résultats !!"):
                    st.write(f"**Légende**: {caption}")
                    st.write(f"**Maladies détectées**: {diseases}")
            
            # Optionnellement, effacez le placeholder ou affichez un message différent après l'exécution
            button_placeholder.empty()

with tab4:
    st.header("Statistics")
    df = get_data("SELECT sensor_id, AVG(temperature) as avg_temperature, AVG(humidity) as avg_humidity FROM sensors GROUP BY sensor_id")
    if not df.empty:
        st.write(df)
    else:
        st.write("No data available.")
