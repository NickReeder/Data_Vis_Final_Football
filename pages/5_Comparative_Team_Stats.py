import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.subplots as sp
import os
import json
import seaborn as sns

import sys
sys.path.append('../')

with open('data/NFL_Stats.json', 'r') as f:
  data = json.load(f)

team_code_dict = {
'ARZ':	'Arizona Cardinals',
'ATL':	'Atlanta Falcons',
'BLT':	'Baltimore Ravens',
'BUF':	'Buffalo Bills',
'CAR':	'Carolina Panthers',
'CHI':	'Chicago Bears',
'CIN':	'Cincinnati Bengals',
'CLV':	'Cleveland Browns',
'DAL':	'Dallas Cowboys',
'DEN':	'Denver Broncos',
'DET':	'Detroit Lions',
'GB':	'Green Bay Packers',
'HST':	'Houston Texans',
'IND':	'Indianapolis Colts',
'JAX':	'Jacksonville Jaguars',
'KC':	'Kansas City Chiefs',
'LV':	'Las Vegas Raiders',
'LAC':	'Los Angeles Chargers',
'LA':	'Los Angeles Rams',
'MIA':	'Miami Dolphins',
'MIN':	'Minnesota Vikings',
'NE':	'New England Patriots',
'NO':	'New Orleans Saints',
'NYG':	'New York Giants',
'NYJ':	'New York Jets',
'PHI':	'Philadelphia Eagles',
'PIT':	'Pittsburgh Steelers',
'SF':	'San Francisco 49ers',
'SEA':	'Seattle Seahawks',
'TB':	'Tampa Bay Buccaneers',
'TEN':'Tennessee Titans',
'WAS':	'Washington Commanders'
}

def build_plots(t_1,t_2):

    r_1 = float(data[t_1]['rush_off_general']['avg_yard'])
    r_2 = float(data[t_2]['rush_off_general']['avg_yard'])

    p_1 = float(data[t_1]['pass_off_general']['avg_yard'])
    p_2 = float(data[t_2]['pass_off_general']['avg_yard'])

    r_1_d = float(data[t_1]['rush_def_general']['avg_yards_conceded'])
    r_2_d = float(data[t_2]['rush_def_general']['avg_yards_conceded'])

    p_1_d = float(data[t_1]['pass_def_general']['avg_yards_conceded'])
    p_2_d = float(data[t_2]['pass_def_general']['avg_yards_conceded'])  

    to_1 = float(data[t_1]['rush_off_general']['turnover_pct'])
    to_2 = float(data[t_2]['rush_off_general']['turnover_pct'])

    to_p_1 = float(data[t_1]['pass_off_general']['turnover_pct'])
    to_p_2 = float(data[t_2]['pass_off_general']['turnover_pct'])


    pct_change = [round(((r_2-r_1)/r_1)*100, 1), round(((p_2-p_1)/p_1)*100, 1),
                  round(((r_2_d-r_1_d)/r_1_d)*100, 1), round(((p_2_d-p_1_d)/p_1_d)*100, 1),
                  round(((to_2-to_1)/to_1)*100, 1), round(((to_p_2-to_p_1)/to_p_1)*100, 1)]
    
    text = [[r_1, str(pct_change[0])+'%', r_2], [p_1, str(pct_change[1])+'%', p_2]
          ,[r_1_d, str(pct_change[2])+'%', r_2_d], [p_1_d, str(pct_change[3])+'%', p_2_d]
          ,[str(round(to_1*100, 1))+'%', str(pct_change[4])+'%', str(round(to_2*100, 1))+'%'], [str(round(to_p_1*100, 1))+'%', str(pct_change[5])+'%', str(round(to_p_2*100, 1))+'%']]

    y_2 = [50*(1 +m/100) for m in pct_change]
    text_pos =[['middle right','top left', 'middle left'] if x >= 0 else ['middle left','top right', 'middle right'] for x in pct_change]

    fig = sp.make_subplots(rows = 3, cols = 2, shared_yaxes=True,
                        subplot_titles=['Offensive Rushing Yards', ' Offensive Passing Yards',
                                       'Defensive Rushing Yards Allowed', ' Defensive Passing Yards Allowed',
                                       'Rushing Turnovers', 'Passing Turnovers'])

    fig.add_trace(go.Scatter(x = [t_1, '', t_2], y = [50, (50 + y_2[0]) / 2, y_2[0]]
                            ,mode ='markers+lines+text', text = [r_1, str(pct_change[0])+'%', r_2]
                            ,textposition= ['top right', 'top center', 'top left']
                            ,name = 'Rushing Yards'
                            ), row = 1, col = 1)
    fig.add_trace(go.Scatter(x = [t_1, '', t_2], y = [50, (50 + y_2[1]) / 2, y_2[1]]
                            ,mode ='markers+lines+text', text = [r_1, str(pct_change[1])+'%', r_2]
                            ,textposition= ['top right', 'top center', 'top left']
                            ,name = 'Passing Yards'
                            ), row = 1, col = 2)
    fig.add_trace(go.Scatter(x = [t_1, '', t_2], y = [50, (50 + y_2[2]) / 2, y_2[2]]
                            ,mode ='markers+lines+text', text = text[2]
                            ,textposition= ['top right', 'top center', 'top left']
                            ,name = 'Rushing Yards'
                            ), row = 2, col = 1)
    fig.add_trace(go.Scatter(x = [t_1, '', t_2], y = [50, (50 + y_2[3]) / 2, y_2[3]]
                            ,mode ='markers+lines+text', text = text[3]
                            ,textposition= ['top right', 'top center', 'top left']
                            ,name = 'Passing Yards'
                            ), row = 2, col = 2)
    fig.add_trace(go.Scatter(x = [t_1, '', t_2], y = [50, (50 + y_2[2]) / 2, y_2[2]] 
                            ,mode ='markers+lines+text', text = [r_1, str(pct_change[2])+'%', r_2]
                            ,textposition= ['top right', 'top center', 'top left']
                            , name = 'Rushing Turnover Percentage'
                            ), row = 2, col = 1)
    fig.add_trace(go.Scatter(x = [t_1, '', t_2], y = [50, (50 + y_2[3]) / 2, y_2[3]] 
                            ,mode ='markers+lines+text', text = [r_1, str(pct_change[3])+'%', r_2]
                            ,textposition= ['top right', 'top center', 'top left']
                            , name = 'Passing Turnover Percentage'
                            ), row = 2, col = 2)


    grid = [[0, 1, 2 ],[3, 4, 5]]
    for i in [1, 2, 3]:
        for j in [1, 2]:
            fig.add_trace(go.Scatter(x = [t_1,  t_1], y = [25, 75]
                                    ,line=dict(color="#000000")
                                    ), row = i, col = j)
            fig.add_trace(go.Scatter(x = [t_2,  t_2], y = [25, 75]
                                    ,line=dict(color="#000000")
                                    ), row = i, col = j)
            
            fig.add_annotation(text = t_1, x = -0.08, y = 50, showarrow= False, row = i, col = j)
            fig.add_annotation(text = t_2, x = 2.08, y = y_2[grid[j-1][i-1]], showarrow= False, row = i, col = j)



    fig.update_traces(hovertemplate = None, hoverinfo = 'skip')

    fig.update_yaxes(range = [25, 75], visible = False, showgrid = False)
    fig.update_xaxes(showgrid = False, visible = False)

    fig.update_layout(margin=dict(l=50, r=50, t=100, b=50)
                    , title_text = 'Head to Head comparison of the ' + team_code_dict[t_1] + ' and the ' + team_code_dict[t_2]
                    ,showlegend = False
                    ,template = 'plotly_white'
                    )
    
    return fig

team_list = ['ARZ','ATL','BLT','BUF','CAR','CHI','CIN','CLV','DAL','DEN','DET',
 'GB','HST','IND','JAX','KC','LV','LAC','LA','MIA','MIN','NE','NO',
 'NYG','NYJ','PHI','PIT','SF','SEA','TB','TEN','WAS']

t_1 = st.sidebar.selectbox('Select First Team', team_list, index=0)
t_2 = st.sidebar.selectbox('Select Second Team', team_list, index=1)

fig = build_plots(t_1,t_2)

st.plotly_chart(fig)