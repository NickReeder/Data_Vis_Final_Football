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
    Research Goal: The goal of VISTA is to provide a tool that allows a user to gather a quick and digestable snapshot of a teams perfomance through a visual medium without compromising on detail. 
    
    Data: Data was collected from PFF Ultimate and contains play-by-play data from every NFL game for the last 10 seasons (2013-2022)

    Please click through the pages to view a more in depth look at each team.

    The first two pages provide an overview of the leauge, comparing each teams overall offensive and defense efficency.
    
    The third page is a ridgeline plot that illustrates the distribution of yards gained on play action, screen, and touchdown passes in a given season.
    
    The fourth page allows the user to compare two teams over a variety of passing and rushing statistics using radar plots.

    The fifth page displays a number of slope plots that the user can use to compare teams offensive and defensive output across a number of variables.

    The sixth shows the user how a teams play calling has varied over time.

    The final page is a glossary of terms.

    



    Thanks & acknowledgements to Dr. Trenton Ford for his help on this project!

    """
)
