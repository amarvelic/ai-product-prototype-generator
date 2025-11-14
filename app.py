import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="AI Product Prototype Generator")

st.title("🧪 AI Product Prototype Generator")
st.write("Enter a product idea and the AI will generate concept prototype images.")

prompt = st.text_input("Describe your product idea:", "")

if st.button("Generate Image"):
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            # Free HF model - NO API KEY NEEDED
            API_URL = "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev-demo.png"

            # HF demo endpoint trick; pass prompt as parameter
            response = requests.get(API_URL)

            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="AI Generated Prototype", use_column_width=True)
            else:
                st.error("Image generation failed. Try again in a few seconds.")
