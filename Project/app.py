import streamlit as st
import sys
# Afficher la version de Python utilisée
st.write(f"Python version: {sys.version}")
from PIL import Image, ExifTags

from transformers import pipeline
import mysql.connector
import pandas as pd
import plotly.express as px




# Initialisation des pipelines Hugging Face
caption_pipeline = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
plant_disease_pipeline = pipeline("image-classification", model="Diginsa/Plant-Disease-Detection-Project")

def generate_caption_and_detect_disease(image):
    # Générer une légende 1ère étape
    caption_result = caption_pipeline(image)
    caption = caption_result[0]["generated_text"]

    # Détection des maladies des plantes 2ème étape
    disease_result = plant_disease_pipeline(image)
    diseases = ", ".join([f"{res['label']}: {res['score']:.2f}" for res in disease_result])

    return caption, diseases

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': 'Sami@2024!',
    'host': '127.0.0.1',
    'database': 'sensor_monitoring',
}

def get_data(query):
    try:
        db_connection = mysql.connector.connect(**db_config)
        df = pd.read_sql(query, db_connection)
        db_connection.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return pd.DataFrame()

def main():
    # Interface Streamlit
    st.title("Analyse des Plantes et Données de Station Météo IoT")

    # Présentation des objectifs du projet
    st.write("Ce projet vise à :")
    st.markdown("""
        - Générer une description contextuelle de l'image.
        - Détecter les maladies des plantes dans l'image.
        - Afficher les données de la station météorologique IoT.
    """)

    # Onglets pour l'analyse des plantes et les données de la station météo
    tab1, tab2, tab3 = st.tabs(["Analyse des Plantes", "Données de Station Météo", "Tableau des Données"])

    with tab1:
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

    with tab2:
        st.header("Données de la Station Météo")
        df = get_data("SELECT * FROM sensors ORDER BY timestamp DESC")
        if not df.empty:
            fig = px.line(df, x='timestamp', y=['temperature', 'humidity'], color='sensor_id', labels={'value': 'Measurements'}, title="Température et Humidité au Fil du Temps")
            st.plotly_chart(fig)
        else:
            st.write("No data available.")

    with tab3:
        st.header("Tableau des Données")
        df = get_data("SELECT * FROM sensors ORDER BY timestamp DESC")
        if not df.empty:
            st.write(df)
        else:
            st.write("No data available.")

if __name__ == '__main__':
    main()
