
import streamlit as st
from PIL import Image
import requests

st.markdown("""
<style>
/* Make metric bigger */
[data-testid="stMetricValue"] {
    font-size: 32px;
}
[data-testid="stMetricLabel"] {
    font-size: 20px;
}

/* Make info box bigger */
.stAlert {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)



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
                    st.metric(label="", value="🤖 Image générée par IA")
                    confidence = proba
                    color = "#F44336"
                else:
                    st.metric(label="", value="📸 Image réelle")
                    confidence = 1 - proba
                    color = "#4CAF50"

                st.markdown(
                    f"<h2 style='color: {color};'>Confiance : {confidence*100:.1f}%</h2>",
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Erreur : {e}")
                st.write(response.text if 'response' in locals() else "Pas de réponse")
