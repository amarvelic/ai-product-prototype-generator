import streamlit as st
import requests
from PIL import Image
import io
import time

st.set_page_config(page_title="AI Product Prototype Generator")

st.title("🧪 AI Product Prototype Generator (Free, No API Key)")
st.write("Enter a product idea to generate a prototype concept image.")

prompt = st.text_input("Describe your product idea:")

generate = st.button("Generate")

# Completely free + anonymous + works without API key
HF_URL = "https://router.huggingface.co/hf-inference/models/prompthero/openjourney"

def generate_image(prompt_text):
    payload = {"inputs": prompt_text}

    response = requests.post(HF_URL, json=payload)

    # If the model is still waking up, retry
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
                except Exception:
                    st.error("Unexpected output. The model may have returned text instead of an image.")
                    st.text(response.text)
            else:
                st.error(f"Generation failed. Status code: {response.status_code}")
                st.text(response.text)
