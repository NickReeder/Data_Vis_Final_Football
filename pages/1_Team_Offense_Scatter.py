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

AFC_E = ['NE', 'BUF', 'MIA', 'NYJ']
AFC_W = ['DEN', 'OAK', 'KC', 'LAC', 'SD', 'LV']
AFC_N = ['BLT', 'CIN', 'CLV', 'PIT'] 
AFC_S = ['IND', 'JAX', 'TEN', 'HST']

NFC_E = ['PHI', 'WAS', 'DAL', 'NYG']
NFC_W = ['SEA', 'LA', 'SF', 'ARZ', 'SL']
NFC_N = ['CHI', 'DET', 'MIN', 'GB']
NFC_S = ['CAR', 'ATL', 'TB', 'NO']

afc = AFC_E + AFC_N + AFC_S + AFC_W
nfc = NFC_E + NFC_N + NFC_S + NFC_W

divs = []
symbol = []
for team in data.keys():
    if team in AFC_E:
        divs.append('AFC East')
        symbol.append('circle')
    elif team in AFC_N:
        divs.append('AFC North')
        symbol.append('circle')
    elif team in AFC_S:
        divs.append('AFC South')
        symbol.append('circle')
    elif team in AFC_W:
        divs.append('AFC West')
        symbol.append('circle')
    elif team in NFC_E:
        divs.append('NFC East')
        symbol.append('diamond')
    elif team in NFC_N:
        divs.append('NFC North')
        symbol.append('diamond')
    elif team in NFC_S:
        divs.append('NFC South')
        symbol.append('diamond')
    elif team in NFC_W:
        symbol.append('diamond')
        divs.append('NFC West')
    else:
        print(team)

rush_off = []
rush_def = []
pass_off = []
pass_def = []
for team in data.keys():
    rush_off.append(data[team]['rush_off_general']['avg_yard'])
    rush_def.append(data[team]['rush_def_general']['avg_yards_conceded'])
    pass_off.append(data[team]['pass_off_general']['avg_yard'])
    pass_def.append(data[team]['pass_def_general']['avg_yards_conceded'])

plotting_data = pd.DataFrame(columns=['team', 'rush_off', 'rush_def', 'pass_off', 'pass_def', 'Divs'])

plotting_data['team'] = data.keys()
plotting_data['rush_off'] = [float(x) for x in rush_off]
plotting_data['rush_def'] = [float(x) for x in rush_def]
plotting_data['pass_off'] = [float(x) for x in pass_off]
plotting_data['pass_def'] = [float(x) for x in pass_def]
plotting_data['Divs'] = divs
plotting_data['Symbol'] = symbol

plotting_data.sort_values(by=['Divs'], inplace= True)
plotting_data.reset_index(inplace = True, drop = True)

rush_off_avg = np.mean(plotting_data['rush_off'])
rush_def_avg = np.mean(plotting_data['rush_def'])
pass_off_avg = np.mean(plotting_data['pass_off'])
pass_def_avg = np.mean(plotting_data['pass_def'])

offense_groups = []
defense_groups = []
for index, row in plotting_data.iterrows():
    if row['rush_off'] > rush_off_avg and row['pass_off'] > pass_off_avg: #Both above average
        offense_groups.append('Both above average')
    elif row['rush_off'] > rush_off_avg: #Only rush offense is above average
        offense_groups.append('Rushing above average')
    elif row['pass_off'] > pass_off_avg: #Only pass offense is above average
        offense_groups.append('Passing above average')
    else: #Both are below average
        offense_groups.append('Both below average')

    if row['rush_def'] > rush_def_avg and row['pass_def'] > pass_def_avg: #Both above average
        defense_groups.append('Both above average')
    elif row['rush_def'] > rush_def_avg: #Only rush offense is above average
        defense_groups.append('Rushing above average')
    elif row['pass_def'] > pass_def_avg: #Only pass offense is above average
        defense_groups.append('Passing above average')
    else: #Both are below average
        defense_groups.append('Both below average')


plotting_data['offense_groups'] = offense_groups
plotting_data['defense_groups'] = defense_groups

sns.set_theme(style = 'white')
sns.set_style('ticks')
sns.set_style({'font.family':'serif', 'font.serif':['Helvetica']})

custom_colors = [
                '#d55e00', # AFC E
                '#0072b2', # AFC N
                '#cc79a7', # AFC S
                '#f0e442', # AFC W
                
                '#d55e00', # NFC E
                '#0072b2', # NFC N
                '#cc79a7', # NFC S
                '#f0e442', # NFC W
        
                ]

fig = px.scatter(plotting_data, x = 'rush_off', y='pass_off',
                 color = 'Divs', 
                 color_discrete_sequence= custom_colors, 
                 symbol= 'Symbol',
                 
                 hover_data={
                     'team':True,
                     'rush_off': True,
                     'pass_off': True,
                     'rush_def': False,
                     'pass_def': False,
                     'Divs': True,
                     'Symbol' : False
                 },
                 labels={
                     'team': 'Team Code',
                     'Divs': 'Division',
                     'rush_off': 'Rushing Output',
                     'pass_off': 'Passing Output'
                 },
                 template = 'plotly_white')

fig.update_traces(
    marker = dict(size = 10)
)

fig.add_hline(y = pass_off_avg, line_color = 'gray', line_dash = 'dash',
              annotation_text = 'League Average',
              annotation_position = 'top left', opacity = 0.7)
fig.add_vline(x = rush_off_avg, line_color = 'gray', line_dash = 'dash',
              annotation_text = 'League Average',
              annotation_position = 'top left', opacity = 0.7)


fig.update_layout(margin=dict(l=30, r=30, t=30, b=30),
                    title = 'Team Offense Scatter Plot',
                    title_font_size = 20,
                    legend_title = 'Division',
                        legend = dict(
                                    bgcolor = 'LightBlue',
                                    bordercolor = 'Black',
                                    borderwidth = 1
                                    ),
                    )

new_names = {'AFC East, circle': 'AFC East', 'AFC North, circle': 'AFC North', 
             'AFC South, circle': 'AFC South', 'AFC West, circle': 'AFC West',
             'NFC East, diamond': 'NFC East', 'NFC North, diamond': 'NFC North', 
             'NFC South, diamond': 'NFC South', 'NFC West, diamond': 'NFC West',}

fig.for_each_trace(lambda t: t.update(name = new_names[t.name]))

fig.update_layout(height=600, width=800)

st.plotly_chart(fig)
