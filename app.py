
import streamlit as st
from PIL import Image
import requests

st.set_page_config(
    page_title="Pixel Truth",
    page_icon="🔍",
    layout="wide"
)

st.title("Pixel Truth")
st.header("Détecteur d'images générées par l'IA")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Choisis une image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image)

with col2:
    st.write("")
    st.write("")
    if st.button('🔍 Prédire', use_container_width=True):
        if uploaded_file is None:
            st.warning("Erreur, image non trouvée")
        else:
            try:
                pixeltruth_api_url =  'https://pixel-truth-326378883173.europe-west1.run.app/predict'
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                with st.spinner('Analyse en cours...'):
                    response = requests.post(pixeltruth_api_url, files=files)
                prediction = response.json()
                proba = prediction["Probability"]
                if proba > 0.5:
                    st.metric(label="Résultat", value="🤖 Image générée par IA")
                    st.info(f"Confiance : {proba*100:.1f}%")
                else:
                    st.metric(label="Résultat", value="📸 Image réelle")
                    st.info(f"Confiance : {(1-proba)*100:.1f}%")
            except Exception as e:
                st.error(f"Erreur : {e}")
                st.write(response.text if 'response' in locals() else "Pas de réponse")
