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
    The overall goal of this project is to create an interactive website to allow coaches and fans to gain
    a useful and concise snapshot into an NFL team's play calling and results as well as that of its
    competitors. The dashboard will provide visuals to allow the user to quickly see the strengths and
    weaknesses of their team overall and against any specific team through a series of meta-statistics
    that we generated. The meta-statistics will look at offensive and defensive outputs as well as
    efficiencies such as first down conversions/preventions.

    ### Potential Plots:
    * Box/Violin Plot
    * Radar Plot
    * Ridge Plot
    * Descriptive Distributions 

    ### Current Plots
    * Radar Plot
    * Ridge Plot (yet to be incorporated into webpage)

-----
# UPDATED INTRODUCTION

The goal of VISTA is to provide the user with a quick and digestable snapshot of a teams perfomance through a visiual medium without comprimising on detail. 
Data was collected from PFF Ultimate and contains data on nearly every play from every NFL game for the last 10 seasons! A series of statistics were generatad,
and are described below.

* Offensive Efficency: The average yards gained per play
* Defensive Efficency: The average yards conceded per play
* First Down Efficency: percentage of plays that convert a first down
* First Down on Fourth Efficency: percentage of plays that convert a first down on fourth down
* Touch Down Efficency: percentage of plays that convert a first down
* Defensive First Down Efficency: percentage of plays that conversion a first down
* Defensive First Down on Fourth Efficency: percentage of plays that do not allow a first down conversion on fourth down

Please click through the pages to view a more in depth look at each team.


Acknolegments to Dr. Trenton Ford for his help on this project


    
    """
)
