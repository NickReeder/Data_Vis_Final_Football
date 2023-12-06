import streamlit as st
import Image

# Load the image
image = Image.open("Ridgeline.png")

# Display the image
st.image(image)