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
    * Ridge Plot
    """
)