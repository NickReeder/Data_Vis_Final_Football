import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout='wide')


hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.write("# Welcome to VISTA: Visual Information System for Team Assessment!")

st.sidebar.success("Select a plot above.")

st.image('https://wallpapercave.com/wp/ZSM48St.jpg')

st.markdown(
    """
    The goal of VISTA is to provide the user with a quick and digestable snapshot of a teams perfomance through a visiual medium without comprimising on detail. 
    Data was collected from PFF Ultimate and contains data on nearly every play from every NFL game for the last 10 seasons!

    Please click through the pages to view a more in depth look at each team.

    The first two pages provide an overview of the leauge, comparing each teams overall offensive and defense efficency.
    
    The third page is a ridgeline plot that____
    
    The fourth page allows the user to compare two teams over a variety of statistics in a radar plot.

    The fifth shows the user how a teams play calling has changed over time.   

    



    Thanks & acknowledgements to Dr. Trenton Ford for his help on this project!

    """
)
