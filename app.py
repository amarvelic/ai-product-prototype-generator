import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

st.title("AI Product Prototype Generator (Free, No API Key)")
st.write("Enter a product idea and AI will generate concept prototype images.")

# Load model once
@st.cache_resource
def load_model():
    model_id = "stabilityai/stable-diffusion-2-1-base"  # Cloud friendly
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32,
        safety_checker=None
    )
    pipe = pipe.to("cpu")  # Runs on free CPU in Streamlit Cloud
    return pipe

pipe = load_model()

prompt = st.text_input("Enter your product idea:", "futuristic bottle with ergonomic grip")

if st.button("Generate"):
    with st.spinner("Generating images... (30–40 seconds)"):
        result = pipe(
            prompt,
            num_inference_steps=20,
            guidance_scale=7.5
        )
        image = result.images[0]

    st.image(image, caption="AI-generated prototype", use_column_width=True)
