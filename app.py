
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
                files = {'file': uploaded_file}
                pixeltruth_api_url = 'https://pixel-truth-326378883173.europe-west1.run.app'
                with st.spinner('Analyse en cours...'):
                    response = requests.post(pixeltruth_api_url, files=files)
                prediction = response.json()
                proba = prediction["Probability"]
                st.write(f"la probabilité est {proba}")
                if proba > 0.5:
                    st.write(f"🤖 Image générée par IA avec({proba*100:.1f}%) de probabilité")
                else:
                    st.write(f"📸 Image réelle avec ({(1-proba)*100:.1f}%) de probabilité")
            except:
                st.error("Erreur de connexion à l'API")
