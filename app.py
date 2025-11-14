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

HF_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

def generate_image(prompt_text):
    payload = {"inputs": prompt_text}

    # Send request to HF
    response = requests.post(HF_URL, json=payload)

    # Model loading fallback (public endpoints take a few seconds to "wake up")
    if response.status_code == 503:
        time.sleep(3)  # wait and retry
        response = requests.post(HF_URL, json=payload)

    return response


if generate:
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            response = generate_image(prompt)

            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                st.image(image, caption="AI Prototype", use_column_width=True)
            else:
                st.error(f"Image generation failed. Status code: {response.status_code}")
                st.error(response.text)
