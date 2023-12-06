import streamlit as st
from PIL import Image

# Load the image
image = Image.open("Ridgeline.png")

# Display the image
st.image(image)