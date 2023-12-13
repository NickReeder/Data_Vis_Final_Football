import streamlit as st

st.write("# Glossary of Terms")

team_list = ['ARZ','ATL','BLT','BUF','CAR','CHI','CIN','CLV','DAL','DEN','DET',
 'GB','HST','IND','JAX','KC','LV','LAC','LA','MIA','MIN','NE','NO',
 'NYG','NYJ','PHI','PIT','SF','SEA','TB','TEN','WAS']

st.markdown(
    """
    A series of statistics were generatad and are described below:

    * Offensive Efficency: The average yards gained per play
    * Defensive Efficency: The average yards conceded per play
    * First Down Efficiency: percentage of plays that convert a first down
    * First Down on Fourth Efficiency: percentage of plays that convert a first down on fourth down
    * Touch Down Efficency: percentage of plays that convert a first down
    * Defensive First Down Efficency: percentage of plays that conversion a first down
    * Defensive First Down on Fourth Efficiency: percentage of plays that do not allow a first down conversion on fourth down

    The following are team codes and the NFL teams they refer to:

    * ARZ = Arizona Cardinals
    * ATL = Atlanta Falcons
    * BLT = Baltimore Ravens
    * BUF = Buffalo Bills
    * CAR = Carolina Panthers
    * CHI = Chicago Bears
    * CIN = Cincinnati Bengals
    * CLV = Cleveland Browns
    * DAL = Dallas Cowboys
    * DEN = Denver Broncos
    * DET = Detroit Lions
    * GB = Green Bay Packers
    * HST = Houston Texans
    * IND = Indianapolis Colts
    * JAX = Jacksonville Jaguars
    * KC = Kansas City Chiefs
    * LV = Las Vegas Raiders
    * LAC = Los Angeles Chargers
    * LA = Los Angeles Rams
    * MIA = Miami Dolphins
    * MIN = Minnesota Vikings
    * NE = New England Patriots
    * NO = New Orleans Saints
    * NYG = New York Giants
    * NYJ = New York Jets
    * PHI = Philadelphia Eagles
    * PIT = Pittsburgh Steelers
    * SF = San Francisco 49ers
    * SEA = Seattle Seahawks
    * TB = Tampa Bay Buccaneers
    * TEN = Tennessee Titans
    * WAS = Washington Commanders
    
    """)