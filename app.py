import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# Title
st.title("AI Product Prototype Generator (Free, No API Key)")
st.write("Enter a product idea and AI will generate concept prototype images.")

# Load model once
@st.cache_resource
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )
    pipe = pipe.to("cpu")  # No GPU required
    return pipe

pipe = load_model()

# User input
prompt = st.text_input("Enter your product idea:", "futuristic water bottle with ergonomic grip")

if st.button("Generate Prototypes"):
    with st.spinner("Generating images... (This may take 20–40 seconds on CPU)"):
        images = pipe(prompt, num_inference_steps=25, num_images_per_prompt=3).images
    
    st.subheader("Generated Prototypes:")
    cols = st.columns(3)
    for col, img in zip(cols, images):
        col.image(img, use_column_width=True)
