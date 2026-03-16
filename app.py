import streamlit as st
from PIL import Image
import requests

st.title("Pixel Truth")
st.write("Upload an image")
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

if st.button('Make prediction'):
    if uploaded_file is None:
        st.warning("Please upload an image")
    else:
        files = {'file': uploaded_file}
        pixeltruth_api_url = 'https://pixel-truth-326378883173.europe-west1.run.app'
        response = requests.post(pixeltruth_api_url, files=files)
        prediction = response.json()
        proba=prediction[0]
        if proba>0.5:
            st.write(f"image fake with probability of {proba}")
        else:
            st.write(f"image real with probability of {1-proba}")
        
