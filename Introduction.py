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

st.markdown(
    """
    The goal of VISTA is to provide the user with a quick and digestable snapshot of a teams perfomance through a visiual medium without comprimising on detail. 
    Data was collected from PFF Ultimate and contains data on nearly every play from every NFL game for the last 10 seasons! A series of statistics were generatad,
    and are described below.

    * Offensive Efficency: The average yards gained per play
    * Defensive Efficency: The average yards conceded per play
    * First Down Efficiency: percentage of plays that convert a first down
    * First Down on Fourth Efficiency: percentage of plays that convert a first down on fourth down
    * Touch Down Efficency: percentage of plays that convert a first down
    * Defensive First Down Efficency: percentage of plays that conversion a first down
    * Defensive First Down on Fourth Efficiency: percentage of plays that do not allow a first down conversion on fourth down

    Please click through the pages to view a more in depth look at each team.

    The first two pages provide an overview of the leauge, comparing each teams overall offensive and defense efficency.
    
    The thrid page is a ridgeline plot that____
    
    The fourth page allows the user to compare two teams over a variety of statistics in a radar plot.

    The fifth shows the user how a teams play calling has changed over time.   





    Thanks & acknowledgements to Dr. Trenton Ford for his help on this project!
)
