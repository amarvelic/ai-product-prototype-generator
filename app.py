import streamlit as st
import requests
from PIL import Image
import io
import time

st.set_page_config(page_title="AI Product Prototype Generator")

st.title("🧪 AI Product Prototype Generator")
st.write("Describe your product idea and generate a product prototype image for free.")

prompt = st.text_input("Enter your product idea:")

generate = st.button("Generate Prototype")

HF_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2-1"

def generate_image(prompt_text):
    payload = {"inputs": prompt_text}

    # Send request to HF
    response = requests.post(HF_URL, json=payload)

    # If model is loading, wait and retry (common for free tier)
    if response.status_code == 503:
        time.sleep(3)
        response = requests.post(HF_URL, json=payload)

    return response


if generate:
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            response = generate_image(prompt)

            if response.status_code == 200:
                try:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="AI Prototype", use_column_width=True)
                except:
                    st.error("Received non-image data from the model.")
                    st.text(response.text)
            else:
                st.error(f"Image generation failed. Status: {response.status_code}")
                st.text(response.text)
