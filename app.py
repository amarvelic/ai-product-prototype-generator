import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="AI Prototype Generator")

st.title("🧪 Free AI Product Prototype Generator (No API Key Needed)")
st.write("Generates design prototypes using a free HuggingFace Space backend.")

prompt = st.text_input("Enter your product idea:")

generate = st.button("Generate")

HF_SPACE_URL = "https://black-forest-labs-flux-1-dev.hf.space/run/predict"

def generate_image(prompt_text):
    payload = {"data": [prompt_text]}
    
    response = requests.post(HF_SPACE_URL, json=payload)
    return response

if generate:
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            response = generate_image(prompt)

            if response.status_code == 200:
                result = response.json()
                # result["data"][0] contains Base64 image
                image_base64 = result["data"][0].split(",")[1]
                image_bytes = base64.b64decode(image_base64)
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Generated Prototype", use_column_width=True)
            el
